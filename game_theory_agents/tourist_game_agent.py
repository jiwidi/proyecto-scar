import spade
import time
import json
import random

XMPP_HOST = 'desktop-tam76sb'


class Strategy:

    def get_offer(self, other_offers):
        raise NotImplemented


class GreedyStrategy:

    def get_offer(self, other_offers):
        return sum(other_offers) / len(other_offers) - 1


class KindleStrategy:

    def get_offer(self, other_offers):
        return sum(other_offers) / len(other_offers)


class SillyStrategy:

    def get_offer(self, other_offers):
        return sum(other_offers) / len(other_offers) + 1


class AgenteEnv(spade.agent.Agent):

    async def setup(self):
        self.other_offers = [random.randint(90, 100)]
        self.current_offer = 100

        template = spade.template.Template(metadata={"performative": "PUSH"})
        self.add_behaviour(self.NegociarBehaviour(), template)

    class NegociarBehaviour(spade.behaviour.CyclicBehaviour):

        async def run(self):
            self.agent.current_offer = self.agent.strategy.get_offer(self.agent.other_offers)

            body = json.dumps({"offer": self.agent.current_offer})
            msg = spade.message.Message(to=f"{self.agent.other_agent}@{XMPP_HOST}", body=body, metadata={"performative": "PUSH"})
            await self.send(msg)

            msg = await self.receive(timeout=60)
            if msg:
                body = json.loads(msg.body)
                other_offer = body.get('offer')
        
                if self.agent.current_offer > other_offer:
                    result = other_offer - 2            
                elif self.agent.current_offer < other_offer:
                    result = self.agent.current_offer + 2
                else:
                    result = self.agent.current_offer

                print(len(self.agent.other_offers), self.agent.strategy.__class__.__name__, result)

                self.agent.other_offers.append(other_offer)
            
            if len(self.agent.other_offers) == 100:
                exit()

        
def main():
    agent_one = AgenteEnv(f"agent_one@{XMPP_HOST}", "env_password")
    agent_one.strategy = GreedyStrategy()
    agent_one.other_agent = 'agent_two'
    agent_two = AgenteEnv(f"agent_two@{XMPP_HOST}", "env_password")
    agent_two.strategy = GreedyStrategy()
    agent_two.other_agent = 'agent_one'

    agent_one.start()
    agent_two.start()
    time.sleep(10)

if __name__ == '__main__':
    main()