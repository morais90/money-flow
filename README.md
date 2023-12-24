## MoneyFlow

MoneyFlow é um framework de fluxo de pagamentos que permite vocês compor as regras de negócio para qualquer cenário de pagamento!

- [MoneyFlow](#moneyflow)
  - [Características arquiteturais](#características-arquiteturais)
  - [Arquitetura](#arquitetura)
  - [Design](#design)
  - [Requirementos para iniciar o projeto](#requirementos-para-iniciar-o-projeto)
  - [Rodando o projeto (veja os requirementos)](#rodando-o-projeto-veja-os-requirementos)
  - [Parando os serviços](#parando-os-serviços)

### Características arquiteturais

MoneyFlow foi desenhado como um sistema distribuído considerando as seguintes características arquiteturais:

**Flexibilidade**
Entendemos que as regras de negócio para o fluxo de pagamento mudam com frequência, por isso o sistema precisa ser flexível para se adaptar as mudanças.

**Manutenibilidade**
Mudanças não podem ser dolorosas de serem feitas, elas precisam ser ágeis e fáceis. O sistem foi desenhado para que de uma forma modular para que o acoplamento de código não torne a manutenção do sistema um pesadelo.

**Escalabilidade**
Escalabilidade operacional e sistêmica precisam andar lado a lado com a evolução do sistema. Atender o progresso de novas funcionalidades e suportar o crescimento da equipe são questões importantes para o projeto.

### Arquitetura

```mermaid
C4Context
    title MoneyFlow framework

    Enterprise_Boundary("context", "System diagram") {
        System(event, "Evento de pagamento", "Um canal arbritário de notificação de <br> pagamento (API, event bus, web interface)")

        Enterprise_Boundary(composerSystem, "Compositor de regras") {
            System(composerUI, "Canvas", "Interface web para visualmente compor as regras de <br>negócio para o fluxo de pagamento do cliente.")
            System(composerAPI, "API de composição de regras", "API web responsável pelo tratamento das regras de <br>negócio do fluxo de pagamento.")
            SystemDb(composerDB, "Banco de dados", "Banco de dados da API de composição")
        }

        System(router, "Roteador", "Contextualiza o evento de pagamento e <br> encaminha para o fluxo de orquestração.")
        System(maestro, "Orquestrador", "Gerencia a regra de pagamento orquestrando a execução dos<br> fluxos de pagamento basedo na regra de composição.")

        Boundary(workflows, "Fluxos") {
            Boundary("product", "Fluxo de produtos") {
                System_Ext(workflowProduct, "Produtos Físico", "Fluxo de pagamento para <br> produtos físicos")
            }

            Boundary("digitalProduct", "Fluxo de produtos digitais") {
                System_Ext(workflowDigitalProduct, "Produtos Digitais", "Fluxo de pagamento <br> para produtos digitais")

            }

            Boundary(subscription, "Fluxo de assinaturas") {
                System_Ext(workflowSubscription, "Assinaturas", "Fluxo de pagamento <br> para assinaturas")
            }

            Boundary("services", "Fluxo de serviços") {
                System_Ext(workflowServices, "Serviços", "Fluxo de pagamento <br> para serviços")
            }
        }

        Rel(composerUI, composerAPI, "Utiliza")
        Rel(event, router, "Envia um evento de pagamento")
        Rel(router, composerAPI, "Consulta as regras de <br> composição de pagamento")
        Rel(router, maestro, "Envia evento de pagamento com <br> a regra de negócio do cliente")

        Rel(maestro, workflowProduct, "Executa")
        Rel(maestro, workflowDigitalProduct, "Executa")
        Rel(maestro, workflowSubscription, "Execute")

        UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="2")
    }
```

### Design

O design do projeto é baseado na idealização de um framework de pagamento. A ideia central do framework é propopr uma interface comum para um fluxo arbritário de pagamento, onde o negócio pode compor as regras de acordo com a necessidade do cliente.

O framework propoe alguns atores como coadjuvenvantes para o funcionamento do fluxo de pagamento. São eles:

**Compositor de regras**

Responsável por compor as regras de negócio para o fluxo de pagamento do cliente. O compositor é uma interface web que permite a visualização e edição das regras de negócio. A interface é composta por um canvas onde o usuário pode arrastar e soltar os componentes de regras de negócio para compor o fluxo de pagamento. O compositor é responsável por persistir as regras de negócio no banco de dados.

A interface deve seguir um modelo de componentes no estilo fluxograma, onde cada componente representa uma regra de negócio, cada componente pode ser conectado a outros componentes para compor o fluxo de pagamento definindo as interações entre os componentes.

Exemplo:

```mermaid
flowchart TD
    A[Pagamento produto físico] --> B(Gerar remessa)
    B --> C{É um livro?}
    C -->|Sim| D[Duplicar a remessa]
    C -->|Não| G[Seguir fluxo]
    D --> F[Notificar departamento de royalties]
    F --> G[Gerar comissão]
```

- O sistema de componentes deve seguir um fluxo aciclíco, onde o fluxo de pagamento é definido por uma sequência de componentes que se conectam entre si.
- O sistema de componentes deve permitir dependências entre componentes, onde um componente pode depender de outro componente para ser executado.
- O sistema de componentes deve ser tolerante a falhas, onde um componente pode falhar e o fluxo de pagamento deve ser capaz de se recuperar da falha e continuar a execução do fluxo de pagamento.

```mermaid
C4Component
    title Payment Composer - Components

    Enterprise_Boundary(components, "Componentes") {
        Component(api, "Composer API", "API de composição de regras")
        Component(ui, "Composer UI", "Interface web para composição de regras")
        Component(db, "Composer DB", "Banco de dados da API de composição")
    }
```

**Roteador**

Dado uma entrada de pagamento e composição do cliente para o pagamento do contexto recebido o roteador é responsável por encaminhar o evento de pagamento para o fluxo de pagamento adicionando o contexto do cliente e a regra de negócio para o pagamento em especifico.

```mermaid
C4Component
    title Payment Router - Components

    Enterprise_Boundary(components, "Componentes") {
        Container_Boundary(api, "Payment Router API") {
            Component(auth, "Authorization", "Identidade e Permissionamento")
            Component(router, "Router System", "Roteamento de eventos de pagamento")
            Component(queue, "Queue", "Fila de eventos de pagamento")
        }
    }

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

**Orquestrador**

O orquestrador é a camada responsável por garantir a correta composição da regra de negócio do cliente. Conectando os fluxos e fazendo o acompanhando da execução. Pense no orquestrador como um maestro de uma orquestra, onde cada fluxo é um instrumento e o maestro é responsável por garantir que cada instrumento seja tocado na ordem correta e no momento certo.

- O orquestrador deve ser capaz de executar os fluxos de pagamento em paralelo.
- O orquestrador deve ser capaz de executar e lidar com falhas de execuçãos nos fluxos.
- O orquestrador deve ser capaz de entender as dependências entre os componentes dos fluxos e garantir a execução na ordem correta.
- O orquestrador deve ser capaz de monitorar e notificar o estado de execução dos fluxos.

```mermaid
C4Component
    title Workflows - Components

    Enterprise_Boundary(components, "Componentes") {
        Component(orchestratorSystem, "Orchestrator System", "Orquestrador de fluxos de pagamento")
        Component("workflows", "Workflows", "Fluxos de pagamento")
        Component(queue, "Queue", "Fila de eventos de pagamento")
    }

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

**Fluxos**

Os fluxos são a parte operacional do framework onde os componentes são executados. Cada fluxo é responsável por garantir a correta execução dos componentes que compoem a regra de negócio do cliente. Tomando conta da ordem de execução, dependências, falhas e comunicação entre os componentes.

- Os fluxos devem ser capazes de executar os componentes em sequência.
- Os fluxos devem ser capazes de executar e lidar com falhas de execução dos componentes.
- Os fluxos devem ser idempotentes, se executados multiplas vezes devem produzir o mesmo resultado.
- Os fluxos devem ser resilientes a falhas, se um componente falhar o fluxo deve ser capaz de se recuperar e continuar a execução dadas as diretrizes de falha para o componente.
- Os componentes dos fluxos deve seguir uma mesma interface de execução, onde cada componente deve receber uma entrada e produzir uma saída.

```mermaid
C4Component
    title Workflows - Components

    Enterprise_Boundary(components, "Componentes") {
        Container_Boundary(nodes, "Nós") {
            Component(nodeCondition, "Node Conditional", "Nós de condicionais")
            Component(nodeTask, "Node Task", "Nós de tarefas")
        }

        Container_Boundary(workflow, "Workflow") {
            Container_Boundary(tasks, "Tasks") {
                Component(taskA, "Task", "Tasks")
                Component(taskB, "Task", "Tasks")
                Component(taskC, "Task", "Tasks")
            }
        }
    }

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### Requirementos para iniciar o projeto

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [pre-commit](https://pre-commit.com/#install)

### Rodando o projeto (veja os requirementos)

```shell
$ docker compose up
```

Após iniciar os serviços você terá disponível os seguintes serviços:

| Serviço              | Accesso                                             |
| -------------------- | --------------------------------------------------- |
| Postgres             | localhost:5432                                      |
| RabbitMQ             | localhost:5672, http://localhost:15672 (Management) |
| Payment Composer API | http://localhost:8000/docs                          |
| Payment Composer UI  | http://localhost:5173                               |
| Payment Router       | http://localhost:8001/docs                          |
| Orchestrator         | Somente worker                                      |

### Parando os serviços

```shell
$ docker compose stop
```

Para parar os serviços e remover os volumes é necessário executar o seguinte comando:

```shell
$ docker compose down -v
```

:warning: **Atenção**: Este comando irá remover todos os volumes dos serviços, incluindo o banco de dados e o RabbitMQ. Tenha certeza que você deseja remover os volumes antes de executar este comando.
