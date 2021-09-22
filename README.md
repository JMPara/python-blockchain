## Overview

This project was created following David Joseph Katz's blockchain and cryptocurrency course.  I have completed the backend portion of this project
and so far it has helped me to get a better understanding of how blockchains and cryptocurrencies function, it has also helped to further my understanding
of data structures, object-oriented programming, and cryptography.

I will continue to work on the frontend portion of this project.

*John-Michael Paraiso*


**Activate the virtual environment**
'''
source blockchain-env/bin/activate
'''

**Install all packages**
'''
pip3 install -r requirements.txt
'''

**Run the tests**

Make sure to activate the virtual environment
'''
python3 -m pytest backend/tests
'''

**Run the application and API**

Make sure to activate the virtual environment
'''
python3 -m backend.app
'''

**Run the peer instance**

Make sure to activate the virtual environment
'''
export PEER=True && python3 -m backend.app
'''