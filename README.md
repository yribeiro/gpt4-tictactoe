# GPT4 TicTacToe

Play TicTacToe against ChatGPT!

## Installation

Clone the repository into a local directory and `cd` into it:

```bash
git clone git@github.com:yribeiro/gpt4-tictactoe.git
cd ./gpt4-tictactoe
```

Create a python virtual environment using:

```bash
python3 -m venv .venv
```

Install the necessary requirements from `requirements.txt` file:

```bash
pip3 install -r requirements.txt
```

## Getting Started

The application requires a valid OpenAPI key to be root folder of the repository.

Create an `.env` file in the root repository.

```bash
touch ./.env
```

Enter the following contents:

```yaml
OPENAI_API_KEY=<ENTER_YOUR_KEY>
```

## Launch the TicTacToe WebApp

Activate the virtual environment using

```bash
source ./.venv/bin/activate
```

Launch the server using the `streamlit` commands:

```bash
streamlit run main.py
```

Your default browser should open up to the default app page.

<img src="https://github.com/yribeiro/gpt4-tictactoe/blob/main/docs/imgs/homescreen.png?raw=true"/>

## Beat ChatGPT

Enter `X` and hit `Enter` to start playing:

</img>

Enter your first move from the choices:

`[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]`

E.g. `2, 2` and hit `Enter`

<img src="https://github.com/yribeiro/gpt4-tictactoe/blob/main/docs/imgs/choosex.png?raw=true"/>

ChatGPT will response and the board will get drawn.

<img src="https://github.com/yribeiro/gpt4-tictactoe/blob/main/docs/imgs/chatgptmove.png?raw=true"/>

Continue entering moves, till the game is over.

<img src="https://github.com/yribeiro/gpt4-tictactoe/blob/main/docs/imgs/finalmove.png?raw=true"/>

Hit `Ctrl+F5` to refresh the app and start a new game!
