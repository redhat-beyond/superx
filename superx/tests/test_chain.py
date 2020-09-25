from models import *
from app import app



def test_add_chain():
    app.config['TESTING'] = True
    
    test_chain = Chain(name='fake-chain')
    db.session.add(test_chain)
    db.session.commit()
    validate_chain = Chain.query.get(test_chain.id)
    assert validate_chain.name == 'fake-chain'
    Chain.query.filter(Chain.id == validate_chain.id).delete()
    db.session.commit()
