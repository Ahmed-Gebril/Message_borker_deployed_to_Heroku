import sys
#only 'tests' module is present in sys path for package lookup
#adding outer level to import from root  folder.
sys.path.append('..')
sys.path.append('.')
from apigateway import state_exists,get_current_state,add_state,remove_state,get_redis_state


state_key = 'test_state'

def test_state_exists_before_add():
    """Checks if state exists boolean when no state is added on initialization.
    """
    assert state_exists(state_key) == False

def test_get_current_state_before_add():
    """Checks for get_current_state to be False when no state is present at the begining.
    """
    assert get_current_state(state_key) == False

def test_add_state_or_test_get_current_state():
    """Checks for add_state to add a new state and 
        where state_exists should be True and 
        current_state `state` key should return added state value.
    """
    add_state('TEST',state_key)
    assert state_exists(state_key) == True
    assert get_current_state(state_key)['state'] == 'TEST'
    
    remove_state(state_key)


def test_remove_state():
    """Checks for state_exists and get_current_state to be False 
    when a new state is added and then removed.
    """
    add_state('TEST',state_key)
    assert state_exists(state_key) == True
    assert get_current_state(state_key)['state'] == 'TEST'
    remove_state(state_key)
    assert state_exists(state_key) == False

def test_state_exists_after_add():
    """Checks for state_exists to be true after a state is added.
    """
    add_state('TEST',state_key)
    assert state_exists(state_key) == True
    remove_state(state_key)

def test_get_current_state_after_add():
    """Checks for current state to return newly added state value.
    """
    add_state('TEST',state_key)
    assert get_current_state(state_key)['state'] == 'TEST'
    remove_state(state_key)

def test_same_state_add_as_previous():
    """
        Checks for lenght of stored data before and after same data is stored.
        If new data is same from previous data it shouldn't be stored again.
    """
    add_state('TEST1',state_key)
    add_state('TEST2',state_key)

    data = get_redis_state(state_key)

    #adding same state as previous
    add_state('TEST2',state_key)
    _data = get_redis_state(state_key)

    assert len(data) == len(_data)

    remove_state(state_key)

def test_get_redis_state():
    """Checks for newly added data value in get_redis_state along with its length.
    """
    add_state('TEST1',state_key)
    add_state('TEST2',state_key)
    data = get_redis_state(state_key)
    assert len(data) == 2
    assert data[0]['state'] == 'TEST1'
    assert data[1]['state'] == 'TEST2'
    remove_state(state_key)
