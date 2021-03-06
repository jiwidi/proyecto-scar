import spade
import time

class AgenteEnv(spade.agent.Agent):

    async def setup(self):
        self.add_behaviour(self.EnviarBehaviour())
        template = spade.template.Template(metadata={"performative": "PUSH"})
        self.add_behaviour(self.RecvBehaviour(), template)

    class EnviarBehaviour(spade.behaviour.OneShotBehaviour):

        async def run(self):
            print("Enviar")
            body = json.dumps({"mensaje":"hola"})
            msg = spade.message.Message(to="agente_env@desktop-tam76sb", body=body, metadata={"performative": "PUSH"})
            await self.send(msg)

    class RecvBehaviour(spade.behaviour.OneShotBehaviour):

        async def run(self):

            msg = await self.receive(timeout=2)
            if msg:
                body = json.loads(msg.body)
                print(body["mensaje"])     
        
def main():
    enviar = AgenteEnv("agente_env@desktop-tam76sb", "env_password")
    enviar.start()
    time.sleep(10)

if __name__ == '__main__':
    print("Iniciar")
    main()