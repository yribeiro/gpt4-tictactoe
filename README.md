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
