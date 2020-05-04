from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import AccessTokenRefreshError
from httplib2 import ServerNotFoundError
from django.db import DatabaseError
from .models import AnalyticsAccount, AnalyticsProperties, \
                    AnalyticsViews, LogEvents
import time
    
class AnalyticsApi():

    def __init__(self, secrets, userid):
        self.user_secrets = secrets
        self.userid = userid
        self.api_name = 'analytics',
        self.api_version = 'v3',
        self.scope = ['https://www.googleapis.com/auth/analytics.readonly']
    
    def log(self, msg, timeresponse):
        """ Method to log messages in database
            Args:
                msg: Success or failure messagge to be stored in database
                timeresponse: The response time to perform a task
            Returns:
                None
        """
        # Log error in database
        log_model = LogEvents(userid=self.userid, 
                              logdescription=msg,
                              timeresponse=timeresponse)
        log_model.save()
        

    def get_service(self):
        """ Initiate a service that communicates to a Google API.
            Args:
                None
            Returns:
                A service that is connected to the specified API.
                In case of error returns None
        """
        start = time.time()
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                self.user_secrets, scopes=self.scope)

            # Build the service object.
            service = build(self.api_name, self.api_version, credentials=credentials)
            self.log("[SUCCESS]: Serviço construído com sucesso.", str(time.time() - start))
            return service
        except TypeError as error:
            # Handle errors in constructing a query.
            error_msg = {'ERROR': ('Erro encontrado ao tentar buscar os dados  : %s' % error) }

            # Log errors in database
            self.log(error_msg, str(time.time() - start))
            return None

        except HttpError as error:
            # Handle API errors.
            error_msg = {'ERROR': ('Arg, foi encontrado um erro na API : %s : %s' % \
                (error.resp.status, error._get_reason()))}
            
            self.log(error_msg, str(time.time() - start))
            return None

        except AccessTokenRefreshError:
            # Handle Auth errors.
            error_msg = {'ERROR': 'As credenciais foram revogadas ou estão expiradas, execute \
                a aplicação novamente para renovar as credenciais.'
                }

            self.log(error_msg, str(time.time() - start))
            return None
        
        except ServerNotFoundError as error:
            # Handle server not found errors
            error_msg = {'ERROR': error}
            
            # Log error in database
            self.log(error, str(time.time() - start))
            return None
        
        except:
            # Non mapped error
            # Log error in database
            self.log('ERROR: Verifique os dados do usuário, possível má formação nas credenciais de acesso.',
                     str(time.time() - start))
            return None
    
    def get_data(self, service):
        """ Method to retrieves all users, properties 
            and views from a given analytics credentials
            Args:
                service: A authenticate service to get data from API
            Returns:
                True: if everything it's ok
                False: otherwise
        """
        start = time.time()
        try:
            # Accounts returned from API
            accounts = service.management().accounts().list().execute() 
        except TypeError as error:
            # Handle errors in constructing a query.
            error_msg = {'ERROR': ('Erro encontrado ao tentar buscar os dados : %s' % error) }

            # Log error in database
            self.log(error_msg, str(time.time() - start))

        except HttpError as error:
            # Handle API errors.
            error_msg = {'ERROR': ('Arg, foi encontrado um erro na API : %s : %s' % \
                (error.resp.status, error._get_reason()))}
            
            # Log error in database
            self.log(error_msg, str(time.time() - start))

        except AccessTokenRefreshError:
            # Handle Auth errors.
            error_msg = {'ERROR': 'As credenciaia foram revogadas ou estão expiradas, execute \
                a aplicação novamente para renovar as credenciais.'
                }
            
            # Log error in database
            self.log(error_msg, str(time.time() - start))
        
        except ServerNotFoundError as error:
            # Handle server not found errors.
            error_msg = {'ERROR': error}    

            # Log error in database
            self.log(error, str(time.time() - start))
        except:
            # Non mapped error
            # Log error in database
            self.log('ERROR: Verifique os dados do usuário, possível má formação nas credenciais de acesso.',
                     str(time.time() - start))

        if accounts.get('items'):
            
            for account in accounts['items']:

                try:
                    # Save or update account informations in database
                    AnalyticsAccount.objects.update_or_create(accountid=account['id'],
                                                              user_id=self.userid,
                                                              defaults={'user_id': self.userid,
                                                                        'owner': accounts['username'],
                                                                        'accountid': account['id'],
                                                                        'name': account['name'],
                                                                        'permissions': account['permissions']})
                    account_model = AnalyticsAccount.objects.filter(accountid=account["id"], \
                         user_id=self.userid).order_by('-pk').get()
                except DatabaseError as e:
                    # log error in database and return False
                    self.log(e +' ao salvar a conta: ' + account['name'], str(time.time() - start))

                # Properties
                webproperties = service.management().webproperties().list(
                     accountId=account['id']).execute()

                if webproperties.get('items'):

                    for prop in webproperties['items']:
                       
                        try:
                            # Save or update properties informations in database
                            AnalyticsProperties.objects.update_or_create(propid=prop["id"],
                                                                         userid=self.userid,
                                                                         defaults={'accountid': account_model,
                                                                                   'propid': prop["id"], 
                                                                                   'name': prop["name"],
                                                                                   'level': prop["level"],
                                                                                   'site': prop["websiteUrl"],
                                                                                   'industry': prop["industryVertical"],
                                                                                   'userid': self.userid})

                            properties = AnalyticsProperties.objects.filter(propid=prop["id"], \
                                userid=self.userid).order_by('-pk').get()                      
                        except DatabaseError as e:
                            # log error in database and return False
                            self.log(e +' ao salvar a propriedade: ' + prop['name'], str(time.time() - start))

                        # Views from each propertie
                        views = service.management().profiles().list(accountId=account["id"], 
                            webPropertyId=prop["id"]).execute()
                        if views.get('items'):
                            for view in views['items']:
                                try:
                                    # Save or update views informations in database
                                    AnalyticsViews.objects.update_or_create(viewid=view["id"],
                                                                            userid=self.userid,
                                                                            defaults={'propid': properties,
                                                                            'viewid': view["id"],
                                                                            'viewname': view["name"],
                                                                            'currency': view["currency"],
                                                                            'created': view["created"],
                                                                            'updated': view["updated"],
                                                                            'timezone': view["timezone"],
                                                                            'userid': self.userid})
                                except DatabaseError as e:
                                    # log error in database and return False
                                    self.log(e +' ao salvar a view: ' + view['name'], str(time.time() - start))
                        else:
                            self.log('A API não retornou dados de views', str(time.time() - start))
        else:
            # If API doesn't returns data
            # log error in database and return False
            self.log('A API não retornou dados.', str(time.time() - start))
           
    def main(self):
        # Authenticate and construct service.
        start = time.time()
        service = self.get_service()
        if service:       
            self.get_data(service)
            self.log("[SUCCESS]: Chamda da API processada com sucesso", str(time.time() - start))
        else:
            self.log("[ERROR]: Erro na chamada da API", str(time.time() - start))
            return False