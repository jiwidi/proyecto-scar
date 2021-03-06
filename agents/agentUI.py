import spade
import time
import json
import argparse

XMPP_HOST = 'host.docker.internal'
FORMAT_AGENT = 'format_agent'

class AgenteEnv(spade.agent.Agent):

    async def setup(self):
        self.add_behaviour(self.EnviarBehaviour())
        template = spade.template.Template(metadata={"performative": "PUSH"})
        self.add_behaviour(self.RecvBehaviour(), template)

    def set_query_args(self, args):
        self.query_args = args

    class EnviarBehaviour(spade.behaviour.OneShotBehaviour):

        async def run(self):
            print("Enviar")
            body = json.dumps({"movies_query": self.build_query()})
            msg = spade.message.Message(to=f"agente_env@{XMPP_HOST}", body=body, metadata={"performative": "PUSH"})
            await self.send(msg)

        def build_query(self):
            query = "select * from df"

            filters = []
            if self.agent.query_args.title:
                filters.append(f"title like '%{self.agent.query_args.title}%'")
            if self.agent.query_args.genre:
                filters.append(f"genres like '%{self.agent.query_args.genre}%'")

            if filters:
                query += " where " + " and ".join(filters)

            return query

    class RecvBehaviour(spade.behaviour.OneShotBehaviour):

        async def run(self):

            msg = await self.receive(timeout=2)
            if msg:
                body = json.loads(msg.body)
                print(f'We received a message with: {body}. Resending it to {FORMAT_AGENT}@{XMPP_HOST}.')
            msg.to = f"{FORMAT_AGENT}@{XMPP_HOST}"
            await self.send(msg)
        
def main(query_args):
    agent = AgenteEnv(f"agente_env@{XMPP_HOST}", "env_password")
    agent.set_query_args(query_args)
    agent.start()
    time.sleep(10)

if __name__ == '__main__':
    print("Iniciar")
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str)
    parser.add_argument('--genre', type=str)
    args = parser.parse_args()

    main(args)