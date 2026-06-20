# Better Hever Discounts

A Python utility that automates loading your Hever card multiple times in order to maximize the discount percentage available through Hever's loading system.

## Why?

Hever offers higher discount percentages when smaller amounts are loaded. Instead of manually performing multiple loads, this script automates the process.

Using it during regular months may increase your discount by up to **5% additional discount**
(if before you were loading at 28%, and now you load at 33%)

Unlike other Hever API repos, this script is very short, making it easy to confirm there is no fraudulent activity.
Additionally,
it only uses pyautogui and is not based on reading the site's code, making it more legitimate from a legal standpoint.

## Features

- Supports both Hever card types
- Calculates optimal load amounts based on your current load percentage
- Reduces repetitive manual form filling

## Requirements

- Python 3
- `pyautogui`

Install dependencies:

```bash
pip install pyautogui
```

## Usage

```bash
python hever_discount_script.py \
    --load-count 4 \
    --card-type food \
    --current-discount-percentage 0.3 \
    --card-number 5555555555554444 \
    --year 2030 \
    --month 03 \
    --cvv 737
```

## Warning

⚠️ According to Hever's EULA, performing more than **5 loads** may result in your card being frozen for 24 hours.

⚠️ The Hever site may update and break this script

## How It Works

The script uses image recognition and mouse & keyboard control to:

1. Open the browser
2. Log on to Hever
3. Locate relevant fields and buttons
4. Fill in payment information
5. Submit repeated loads automatically

## Legality

Hever's EULA acknowledges this loading feature, so it seems fair to use it.
This script just automates the process of manually filling out information.
The Hever EULA doesn't mention automation and the site does not use CAPTCHA, meaning it isn't trying to deter bots. 

## License

This project is licensed under the **GPL-3.0 License**.

See the [LICENSE](LICENSE) file for details.

---

