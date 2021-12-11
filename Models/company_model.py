from Database.accessor import DbAccessor
from Database.Entities.entities import Company

class CompanyModel:
    def create(self, company_name):
        self.session = DbAccessor().create_session()
        try:
            company = Company(
                    company_name = company_name, 
                )
            self.session.add(company)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def delete(self, company_name):
        self.session = DbAccessor().create_session()
        try:
            company = self.session.query(Company).filter(
                Company.company_name == company_name
            ).one()
            self.session.delete(company)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def update(self, old_name, company_name):
        self.session = DbAccessor().create_session()
        try:
            if (company := self.session.query(Company).filter(
                    Company.company_name == old_name
                ).first()
            ):
                company.company_name = company_name
                self.session.commit()
            else:
                raise ValueError('company not found')
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def read(self):
        self.session = DbAccessor().create_session()
        companies = self.session.query(
            Company.id,
            Company.company_name
        ).all()
        self.session.close()
        return companies


