from sqlalchemy import create_engine,Table,Column,Integer,String,ForeignKey,Text
from sqlalchemy.orm import sessionmaker,declarative_base,relationship

engine=create_engine("postgresql://gireesh:1111@localhost:5432/solutionhub")
Base=declarative_base()

class SignUp(Base):
    __tablename__="signups"

    signup_id=Column(Integer,primary_key=True)
    first_name=Column(String(length=255))
    last_name=Column(String(length=255))
    email=Column(Text)
    password=Column(Text)
    retype_password=Column(Text)

    def __repr__(self):
        return "<SignUp(signup_id='{0}',first_name='{1}',last_name='{2}',email='{3}',password='{4}')>".format(self.signup_id,self.first_name,self.last_name,self.email,self.password)

class Login(Base):
    __tablename__="logins"

    login_id=Column(Integer,primary_key=True)
    signup_id=Column(Integer,ForeignKey('signups.signup_id'))
    email=Column(Text)
    password=Column(Text)

    s=relationship('SignUp')

    def __repr__(self):
        return "<Login(login_id='{0}',signup_id='{1}',email='{2}',password='{3}')>".format(self.login_id,self.signup_id,self.email,self.password)

class Topic(Base):
    __tablename__="topics"

    topic_id=Column(Integer,primary_key=True)
    title=Column(String(length=255))

    def __repr__(self):
        return "<Topic(topic_id='{0}',title='{1}')>".format(self.topic_id,self.title)
    
class Solution(Base):
    __tablename__="solutions"

    solution_id=Column(Integer,primary_key=True)
    topic_id=Column(Integer,ForeignKey('topics.topic_id'))
    description=Column(String(length=255))

    topic=relationship('Topic')

    def __repr__(self):
        return "<Solution(solution_id='{0}',description='{1}')>".format(self.solution_id,self.description)

Base.metadata.create_all(engine)

def create_session():
    Session=sessionmaker(bind=engine)
    return Session()

if __name__=="__main__":
    session=create_session()
    '''
    topic=Topic(title="what is photosynthesis")
    session.add(topic)
    session.commit()

    sol=Solution(description="the process by which green plants and some other organisms use sunlight to synthesize foods from carbon dioxide and water. ",topic_id=topic.topic_id)
    session.add(sol)
    session.commit()
    '''
    #print(topic)
    #print(sol)

    a=SignUp(first_name="raavi",last_name="gireesh",email="gireesh23@gmail.com",password="3456@123",retype_password="3456@123")
    session.add(a)
    session.commit()

    b=Login(signup_id=a.signup_id,email=a.email,password=a.password)
    session.add(b)
    session.commit() 

    print(a)
    print(b)   
    


