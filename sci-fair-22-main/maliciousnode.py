import rsa, json, time, pickle, logging, base64,random
from graphviz import Digraph

class maliciousNode:

    def __init__(self, init=False): # if initial data is false, loads from file; if none, starts new; if given attempts to load initial
        logging.debug("Initializing new Node class")
        if init == False:
            logging.debug("Attempting to load from file...")
            try:
                dictdata = self.load_var()
            except Exception as e:
                logging.error(e)
                dictdata = self.generate_new_info()
                logging.debug("Couldn't load from file, using new data instead.")
        elif init:
            dictdata = init
        else:
            logging.debug("Generating new data...")
            dictdata = self.generate_new_info()

        self.chain = dictdata['chain']  # personal trusted chain, doesn't contain signature but contains last signature
        self.pending = dictdata['pending']
        self.last_work = dictdata['last_work']
        self.winners = dictdata['winners']
        self.next_block = dictdata['next_block']
        self.heard_chain = dictdata['heard_chain']
        self.sk = dictdata['sk']
        self.pk = dictdata['pk']
        self.nickname = dictdata["nickname"]
        self.contacts = dictdata["contacts"]

        logging.debug(f'Initiation completed; class variable are as follows: \nChain: {self.chain}\nPending list: {self.pending}\nLast work: {self.last_work}\nWinners: {self.winners}\nNext block: {self.next_block}\nHeard Chain: {self.heard_chain}\nSecret key: {self.sk}\nPublic key: {self.pk}\nContacts: {self.contacts}\nNickname: {self.nickname}\n')

    def create_fake_block(self,workdata,teaminfo,number_of_winners=1):
        fake_transaction = {
            'sender':'420',
            'recipient':self.pk,
            'amount':'100'
        }

        logging.debug(f'fake transaction created: {fake_transaction}')

        self.pending.append(fake_transaction)

        logging.debug(f'added fake transaction to pending, it looks like this {self.pending}')

        message = self.create_block(workdata,teaminfo,number_of_winners)

        return message

    def create_block(self,work_data,teaminfo,number_of_winners=1):
        logging.debug(f"Creating new block ")

        prev_signature = self.heard_chain[len(self.heard_chain)-1]
        prev_signature = prev_signature['signature']

        block = {
            'index': (len(self.heard_chain)),
            'prev_signature':prev_signature,
            'transactions': self.pending,
            'compensation':self.find_new_work(work_data)
        }

        logging.debug("block created")

        self.pending = []
        self.chain.append(block)

        message = {
            'type':'block',
            'timestamp':time.time(),
            'pk':self.pk,
            'block':block,
            'signature':self.sign(block)
        }

        logging.debug("message created")

        self.winners = self.easy_miner_decider(teaminfo,work_data,number_of_winners)

        self.next_block = message

        return message

    def setnick(self, nick):
        logging.debug(f"appending self public key {self.pk} to contact list")
        self.contacts[self.pk] = nick
        self.nickname = nick

    def transaction(self, recipient, amount):
        logging.debug("Generating new transaction")
        transaction = {
            'sender': self.pk,
            'recipient': recipient,
            'amount': amount,
            'timestamp':time.time()
        }
        message = {
            'type': 'transaction',
            'timestamp': time.time(),
            'pk':self.pk,
            'transaction': transaction,
            'signature': self.sign(transaction),
            "nickname": self.nickname
        }
        return message

    def sign(self, content):
        logging.debug(f"signing {content}")
        encoded = json.dumps(content).encode()
        signedish = rsa.sign(encoded, self.sk, 'SHA-1')

        encodedSignature = base64.b64encode(signedish)
        signed = encodedSignature.decode('ascii')
        return signed

    def process_message(self, input, addr):
        logging.info(f"New message from {addr}:\n{input}")
        print(f"You've recieved a new message from {addr}")


        if input['type'] == 'transaction':

            senderpkn = input['pk']
            senderpk = rsa.PublicKey(senderpkn, 65537)

            transaction = input['transaction']
            transactionCoded = json.dumps(transaction).encode()


            signature = input['signature']
            sigb64 = signature.encode()
            sigbytes = base64.b64decode(sigb64)

            verif = rsa.verify(transactionCoded, sigbytes, senderpk)

            if verif == 'SHA-1':
                logging.debug("signature verified")
                sig_verif = True
            else:
                logging.debug("signature invalid")
                print("Unfortunately, the message signature could not be verified.")
                sig_verif = False

            if float(transaction['amount']) <= self.find_balance(senderpkn) + self.find_pending_balance(senderpkn):
                logging.debug(f"{senderpkn} has the money to send")
                mon_verif = True
            else:
                logging.debug(f"oops, {senderpkn} is a broke ass! they only have {self.find_balance(senderpkn)+self.find_pending_balance(senderpkn)}")
                mon_verif = False

            current_time = time.time()
            max_network_delay = 60*60*24

            if current_time - transaction['timestamp'] < max_network_delay:
                rec_verif = True
            else:
                logging.debug("it was so long ago bruh")
                rec_verif = False

            dou_verif = True
            for t in self.pending:  # prevents you from copy pasting a transaction message and sending it
                if t['timestamp'] == transaction['timestamp'] & t['sender'] == transaction['sender'] & t['recipient'] == transaction['recipient']:
                    dou_verif = False

            if sig_verif == True & mon_verif == True & rec_verif == True & dou_verif == True:  # I think this is a broken and stupid way to do this, L
                self.pending.append(transaction)
                print(input["nickname"])

        elif input['type'] == 'block': # when a miner sees a block

            senderpkn = input['pk']
            senderpk = rsa.PublicKey(senderpkn, 65537)

            signature = input['signature']
            sigb64 = signature.encode()
            sigbytes = base64.b64decode(sigb64)

            block = input['block']
            blockCoded = json.dumps(block).encode()

            if block['index'] == (self.heard_chain[len(self.heard_chain)-1])['index']:
                ex_verif = False
                logging.debug("the same block already exists from some other guy")  # this system is problematic
            else:
                ex_verif = True
                logging.debug("different from parallel ones verified")

            if rsa.verify(blockCoded,sigbytes,senderpk) == 'SHA-1':
                logging.debug("signature verified")
                sig_verif = True
            else:
                logging.debug("signature invalid")
                sig_verif = False

            if self.winners.count(str(input['pk'])) > 0:
                logging.debug("block creator verified")
                cr_verif = True
            else:
                logging.debug("block creator invalid")
                cr_verif = False

            if block == self.chain[len(self.chain)-1]:  # sees if the content matches the newest personal block
                logging.debug("block content correct")
                con_verif = True
            else:
                logging.debug("block content incorrect:")
                logging.debug(f'{block}\ndoes not match\n{self.chain[len(self.chain)-1]}')
                con_verif = False

            logging.debug(f'VERIFICATIONS:\n{ex_verif}\n{sig_verif}\n{cr_verif}\n{con_verif}')
            if ex_verif is True & sig_verif is True & cr_verif is True & con_verif is True:

                block_with_signature = {
                    'index':block['index'],
                    'prev_signature':block['prev_signature'],
                    'transactions':block['transactions'],
                    'compensation':block['compensation'],
                    'signature':signature
                }

                logging.debug(f'the block was approved, added signature and now it looks like this: {block_with_signature}')

                self.heard_chain.append(block_with_signature)

                logging.debug(f'the new chain looks like this: {self.heard_chain}')

                logging.debug("block added")
            else:
                logging.debug("cumulative verification failed")

        elif input['type'] == 'genesis':

            genesisBlock = input['block']

            # trust it completely if you have no blocks so far
            if len(self.heard_chain) == 0:
                self.heard_chain.append({
                    'index':genesisBlock['index'],
                    'prev_signature':genesisBlock['prev_signature'],
                    'transactions':genesisBlock['transactions'],
                    'compensation':genesisBlock['compensation'],
                    'signature':input['signature']
                })

                self.last_work = genesisBlock['compensation']

        elif input['type'] == 'introduction':
            return self.introduce_self(input)

        return True  # this is for response purposes

    def lazy_process(self, message):
        block = message["block"]
        verify_sender = rsa.verify(json.dumps(block).encode(), base64.b64decode(signature := message["signature"].encode()), rsa.PublicKey(message["pk"],65537))
        sender_elected = message["pk"] in self.winners

        indexes = []

        for heard_block in self.heard_chain:
            if heard_block['index'] == block['index'] - 1:
                indexes.append(heard_block)

        can_attach = False

        for index in indexes:
            if block['prev_signature'] == index['signature']:
                can_attach = True

        #  adds block if all conditions ar emet
        if verify_sender == True & sender_elected == True & can_attach == True:
            block_with_signature = {
                'index': block['index'],
                'prev_signature': block['prev_signature'],
                'transactions': block['transactions'],
                'compensation': block['compensation'],
                'signature': signature
            }

            self.heard_chain.append(block_with_signature)
            logging.debug("block added")

        else:
            logging.debug(f"FAILFAILFAIAILFAILFAILFAIL: dfasdjfjdsf\n\n\n{message}\n\n\nBOOOBOOBOBOBHHHOOHOOOOO")


    def genesis(self,fake_work_data):
        block = {
            'index':0,
            'prev_signature':'pistachio',
            'transactions':[],
            'compensation':fake_work_data
        }

        message = {
            'type':'genesis',
            'timestamp':time.time(),
            'pk':self.pk,
            'block':block,
            'signature':self.sign(block)
        }

        self.chain.append(block)

        logging.debug("genesisd")
        return message

    def find_new_work(self,work_data):
        logging.debug("finding how much work ppl did")
        # variable names are confusing so here's the meanings:
        # work_data is what the api function gives, and it gives total work done by users, ordered by work
        # self.last_work is what work_data was when the last block was created
        # current_work_data should be the change in work between last time and this time
        current_work_data = []
        work_data = work_data[1:len(work_data)]
        logging.debug(f'last_work: {self.last_work}')
        logging.debug(f'total work: {work_data}')

        had_existing_work = []  # this is the index for work_data describing people who aren't new

        for i in range(len(work_data)):  # iterates through all the people on the latest api
            row = work_data[i]   # finds name and WUs for each person on api
            name = row[0]
            units = row[4]



            for j in range(len(self.last_work)):  # for each person, go through the previous work data
                worker = self.last_work[j]  # worker stands for a worker in previous work data
                logging.debug(f'checking if id matches {worker}')
                if worker['id'] == name:
                    logging.debug('matched, calculating')
                    new_work_units = units - worker['amount']  # if the old person matches the new person, subtract
                                                               # the old amount from the new amount

                    if new_work_units > 0:  # if there was new work done, add it, and documents who had worked before
                        amount = new_work_units
                        current_work_data.append({
                            'id':name,
                            'amount':amount
                        })

                    had_existing_work.append(i)

        logging.debug(f'workers who had existing work: {had_existing_work}')

        had_existing_work.reverse()

        for already_worked in had_existing_work:
            work_data.pop(already_worked)

        logging.debug(f'people who havent done work before: {work_data}')

        for new_worker in work_data:  # goes through the people that didn't get matched, and adds it
            current_work_data.append({
                'id':new_worker[0],
                'amount':new_worker[4]
            })

        logging.debug(current_work_data)

        self.last_work = current_work_data

        logging.debug(f'current work data: {current_work_data}')

        return current_work_data


    def find_balance(self, userID):
        logging.debug("Finding balance")
        balance = 0

        for i in range(len(self.chain)):
            block = self.chain[i]
            transactions = block['transactions']
            compensations = block['compensation']

            for transaction in transactions:
                sender = transaction['sender']
                recipient = transaction['recipient']
                amount = transaction['amount']

                if sender == userID:
                    balance = balance - amount
                elif recipient == userID:
                    balance = balance + amount

            for compensation in compensations:
                worker = compensation['id']
                units = compensation['amount']
                compensated_amount = units  # for now

                if worker == str(userID):
                    balance = balance + compensated_amount

        return balance

    def visualize_chain(self):

        d = Digraph('chain_visualization')
        i = 0
        for block in self.heard_chain:  # create a rectangle for each block
            i = i+1
            d.node(str(i),'index: ' + str(block['index']),shape='rectangle')


        b = 0
        for block in self.heard_chain:  # connect the blocks with arrows if the signatures match
            b = b+1
            p = 0
            for prev_block in self.heard_chain:
                p = p+1
                if block['prev_signature'] == prev_block['signature']:
                    d.edge(str(p),str(b))

        d.attr(rankdir='LR')

        r = d.render()

        return r

    def visualize_local_chain(self):
        d = Digraph('chain_visualization')
        i = 0
        for block in self.chain:  # create a rectangle for each block
            i = i + 1
            d.node(str(i), 'index: ' + str(block['index']), shape='rectangle')

        d.attr(rankdir='LR')

        r = d.render()

        return r

    def find_pending_balance(self, userID):
        logging.debug("Finding pending balance")
        pending_balance = 0

        for transaction in self.pending:
            if transaction['sender'] == userID:
                pending_balance = pending_balance - transaction['amount']
            elif transaction['recipient'] == userID:
                pending_balance = pending_balance + transaction['amount']

        return pending_balance

    def introduce_self(self,message=False):
        if not message:
            message = {
                'type':'introduction',
                'contacts':self.contacts  # 'public key #':'nickname'
            }
            return message
        else:  # processes message
            new_contacts = message['contacts']
            for pk in new_contacts:
                if int(pk) not in self.contacts:
                    self.contacts[int(pk)] = new_contacts[pk]
            return True


    def miner_decider(self,teaminfo,workinfo,number_of_winners=1):
        # team info from team_info, workinfo from get_members

        work_values = self.find_new_work(workinfo)

        logging.debug(work_values)
        winners = []

        for raffle in range(number_of_winners):
            total_work = 0

            for row in work_values:
                total_work = total_work + float(row['amount'])
            # calculates total ballots

            random.seed(teaminfo['score']+raffle)
            winner = random.randint(1, total_work)

            for i in range(0, len(work_values)):  # this part does the deciding
                miner = work_values[i]
                winner = winner - float(miner['amount'])
                if winner <= 0:
                    winners.append(miner['id'])
                    work_values.pop(i)  # this makes you not get picked twice

        # I sincerely believe that something here is very, very wrong
        logging.debug(f'winners: {winners}')
        return winners

    def easy_miner_decider(self,teaminfo,workinfo,number_of_winners=1):

        # workinfo is an array of arrays with 5 rows: row[0] is id, row [4] is WUs
        logging.debug(workinfo)
        ids = []
        works = []
        winners = []
        for row in workinfo:
            if not row[0] == 'name':
                ids.append(row[0])
                works.append(row[4])  # makes two arrays, with names and work amounts

        logging.debug(ids)
        logging.debug(works)
        logging.debug(number_of_winners)
        for raffle in range(number_of_winners):
            total_work = 0

            for w in works:
                total_work = total_work + w
            logging.debug(f'raffle {raffle}: {total_work} work total')
            # calculates total wus done

            random.seed(teaminfo['score']+raffle)
            picked_number = random.randint(1, total_work)
            logging.debug(f'picked ticket {picked_number}')

            if len(ids) == 1:
                winners.append(ids[0])
            else:
                for i in range(0,len(ids)-1):  # this part does the deciding

                    picked_number = picked_number - float(works[i])
                    logging.debug(f'subtracted work ({works[i]}) from winning number which is now ({picked_number})')
                    if picked_number <= 0:
                        winners.append(ids[i])
                        logging.debug('winner appended')
                        ids.pop(i)
                        works.pop(i)  # this makes you not get picked twice
                        break
                logging.debug(f'remaining ids after raffle {raffle}: {ids}')
                logging.debug(f'remaining works after raffle {raffle}: {works}')

        # I sincerely believe that something here is very, very wrong
        logging.debug(f'winners: {winners}')
        return winners

    def save_var(self, var, filename="storage.txt"):
        with open(filename, 'wb') as f:
            pickle.dump(var, f)

    def load_var(self, filename="storage.txt"):
        logging.debug(f"trying to load file {filename}")
        with open(filename, 'rb') as f:
            loaded = pickle.load(f)
            logging.debug("Loaded data")
            return loaded

    def generate_new_info(self):
        (pk, sk) = rsa.newkeys(512)
        dictdata = {
            'chain': [],
            'pending': [],
            'last_work':[],
            'winners':[],
            'next_block':[],
            'heard_chain':[],
            'sk': sk,
            'pk': pk.n,
            "nickname": "Anonymous",
            "contacts": {}
        }
        return dictdata

    def backup_data(self):
        dictdata = {
            'chain': self.chain,
            'pending': self.pending,
            'last_work':self.last_work,
            'winners':self.winners,
            'next_block':self.next_block,
            'heard_chain':self.heard_chain,
            'sk': self.sk,
            'pk': self.pk,
            "nickname": self.nickname,
            "contacts": self.contacts
        }
        self.save_var(dictdata)