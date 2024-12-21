# EveryText-for-Textboard
Is a bot of the web site textboard.fr . The bot use token for build your ascii art in the map.

---

## 1. Installing Required Packages

Make sure Python is installed on your machine. Then, install the required libraries using the following command:

```bash
pip install json websocket-client tqdm
```

---

## 2. Setting Initial Coordinates and token

Before running the bot, you need to define the starting coordinates for your ASCII art. In the code, modify the following variables:

```python
stx = 0  # Starting x coordinate
sty = 0  # Starting y coordinate
```

And you have to put your token here : 
```python
auth_token = "YOUR AUTH_TOKEN HERE"
```

### Coordinate Illustration

Here is a simple representation of the coordinates:

```
(y)
 |
 | (sty = 0)
 |
 +-------------------- (x)
(stx = 0)
```

---

## 3. Modifying the `ascii_art.txt` File

To generate your custom ASCII art, open the `ascii_art.txt` file in a text editor and replace its content with the ASCII art you want to use.

### Example Content for `ascii_art.txt`:

```
  .-""""-.
 /        \
|          |
 \        /
  '-....-'
```

P.S. All characters are allowed.

---

## 4. Running the Bot

Once the previous steps are complete, run the Python file containing the bot using the following command:

```bash
python main.py
```

The bot will generate the ASCII art based on the coordinates and the content of the `ascii_art.txt` file.

---

## Additional Notes

- Ensure that the `ascii_art.txt` file is in the same directory as the Python script.
- If you encounter errors, check that all libraries are correctly installed and that the `ascii_art.txt` file exists.

Have fun creating and sharing your ASCII art!
