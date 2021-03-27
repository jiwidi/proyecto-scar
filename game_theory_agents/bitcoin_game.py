from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random
import time
import pandas as pd

class BitcoinProposeAgent(Agent):

    async def setup(self):
        print("{} started".format(self.__class__.__name__))
        self.game = self.GameBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.game, template)

    class GameBehaviour(OneShotBehaviour):
        
        async def run(self):
            agent_propose = min(int(random.gauss(55, 5)), 100)
            self.agent.set("agent_propose", agent_propose)
            msg = Message(to=self.agent.get("other_agent_jid"))
            msg.set_metadata("performative", "inform")
            msg.body = str(100-agent_propose)
            print("{} sends its propose: {} (and {} for the other person)".format(self.agent.__class__.__name__, agent_propose, 100-agent_propose))
        

            await self.send(msg)
        
        async def on_end(self):
            print("[{}] {} finished with exit code: {}.".format(self.agent.__class__.__name__, self.__class__.__name__, self.exit_code))
            await self.agent.stop()


class BitcoinReceiveAgent(Agent):

    async def setup(self):
        print("{} started".format(self.__class__.__name__))
        self.game = self.GameBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.game, template)

    class GameBehaviour(OneShotBehaviour):
        
        async def run(self):
            agent_range = [min(int(random.gauss(45, 5)), 50), 100]
            self.agent.set("agent_range", agent_range)
            print("{} accepts a propose in range {}".format(self.agent.__class__.__name__, agent_range))
        
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                propose = int(msg.body)
                print("{} has received a message: {}".format(self.agent.__class__.__name__, msg.body))
                if propose in range(*agent_range):
                    print("{} ACCEPT the propose of {}".format(self.agent.__class__.__name__, propose))
                else:
                    print("{} REFUSE the propose of {}".format(self.agent.__class__.__name__, propose))
            else:
                print("{} has notreceived any message".format(self.agent.__class__.__name__))
                self.kill(-1)
        
        async def on_end(self):
            print("[{}] {} finished with exit code: {}.".format(self.agent.__class__.__name__, self.__class__.__name__, self.exit_code))
            await self.agent.stop()


if __name__ == '__main__':
    df = pd.DataFrame(columns = ['BTC_to_propose_agent', 'BTC_to_receive_agent', 'accept_min', 'accept_max', 'accepted'])

    for i in range(500):
        propose_agent = BitcoinProposeAgent("bitcoin_propose_agent@localhost", "psw1")
        receive_agent = BitcoinReceiveAgent("bitcoin_receive_agent@localhost", "psw2")
        propose_agent.set("other_agent_jid", str(receive_agent.jid))
        receive_agent.set("other_agent_jid", str(propose_agent.jid))

        ra_future = receive_agent.start()
        time.sleep(2)
        pa_future = propose_agent.start()
        ra_future.result()
        pa_future.result()
        receive_agent.game.join()
        propose_agent.game.join()
        receive_range = receive_agent.get("agent_range")
        propose = propose_agent.get("agent_propose")
        df.loc[i] = [propose, 100-propose, *receive_range, 100-propose in range(*receive_range)]
    
    print(df)
    print(df.mean())
    df.to_csv('results_bitcoin_game.csv')
    