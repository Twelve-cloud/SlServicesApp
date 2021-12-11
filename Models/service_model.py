from Database.accessor import DbAccessor
from Database.Entities.entities import Service

class ServiceModel:
    def create(self, service_name, price, company_name):
        self.session = DbAccessor().create_session()
        try:
            service = Service(
                    service_name = service_name,
                    price = float(price),
                    company_name = company_name, 
                )
            self.session.add(service)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def delete(self, service_name, company_name):
        self.session = DbAccessor().create_session()
        try:
            service = self.session.query(Service).filter(
                Service.company_name == company_name, Service.service_name == service_name
            ).one()
            self.session.delete(service)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def update(self, service_name, price, company_name):
        self.session = DbAccessor().create_session()
        try:
            if (service := self.session.query(Service).filter(
                    Service.company_name == company_name, Service.service_name == service_name
                ).first()
            ):
                service.price = float(price)
                self.session.commit()
            else:
                raise ValueError('service not found')
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def read(self, company_name):
        self.session = DbAccessor().create_session()
        services = self.session.query(Service).filter(
                Service.company_name == company_name
        ).all()
        self.session.close()
        return services

    def read_by_service(self, service_name):
        self.session = DbAccessor().create_session()
        services = self.session.query(Service).filter(
                Service.service_name == service_name
        ).all()
        self.session.close()
        return services

    def read_all(self):
        self.session = DbAccessor().create_session()
        services = self.session.query(
                Service.service_name,
                Service.price,
                Service.company_name
        ).all()
        self.session.close()
        return services 





