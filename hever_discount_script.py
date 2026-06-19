import argparse
from dataclasses import dataclass
from time import sleep

import pyautogui

CRITICAL_IMAGE_SEARCH_CONFIDENCE = 0.99
HEVER_MINIMUM_LOAD_VALUE: int = 5  # Sadly the loading system only accepts integers larger than 5
HEVER_MAXIMUM_LOAD_VALUE: int = 1000
HEVER_MAXIMUM_DAILY_LOAD_COUNT = 5


def press_image(image_path: str, confidence: float):
    image_location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    left, top, width, height = image_location
    image_x, image_y = pyautogui.center((left, top, width, height))
    pyautogui.click(image_x, image_y)


def load_once(card_type: str, amount: int, card_number: str, year: str, month: str, cvv: str):
    # go to the checkout site
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite(card_type_to_site_address(card_type))
    pyautogui.press("enter")

    # wait for page to load
    sleep(5)

    # press an image about the amount to load
    press_image(card_type_to_image_above_amount_to_load(card_type), CRITICAL_IMAGE_SEARCH_CONFIDENCE)

    # get to amount to load
    pyautogui.press('tab')
    pyautogui.typewrite(str(amount))

    # accept the EULA
    pyautogui.press('tab')
    pyautogui.press('space')

    # skip reading the EULA
    pyautogui.press('tab')

    # get to card number field
    pyautogui.press('tab')
    pyautogui.typewrite(card_number)

    # get to card year field
    pyautogui.press('tab')
    pyautogui.typewrite(year)

    # get to card month field
    pyautogui.press('tab')
    pyautogui.typewrite(month)

    # get to card cvv field
    pyautogui.press('tab')
    pyautogui.typewrite(cvv)

    # go off the fields so that the card can be checked
    pyautogui.press('tab')

    # wait for the card to be checked
    sleep(5)

    # submit
    pyautogui.press('tab')
    pyautogui.press('space')

    # wait for confirmation popup to show up
    sleep(3)

    # confirm
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')


def card_type_to_site_address(card_type: str) -> str:
    if card_type == 'food':
        return "https://www.hvr.co.il/orders/gift_2000.aspx?food=1"
    elif card_type == 'standing':
        return "https://www.hvr.co.il/orders/gift_2000.aspx"
    else:
        raise RuntimeError(f"Unknown card type: {card_type}")


def card_type_to_image_above_amount_to_load(card_type: str) -> str:
    if card_type == 'food':
        return "food_site_above_amount_to_load.png"
    elif card_type == 'standing':
        return "standing_site_above_amount_to_load.png"
    else:
        raise RuntimeError(f"Unknown card type: {card_type}")


def log_into_hever():
    # go to the hever site
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite("https://www.hvr.co.il/")
    # disable auto-complete to not enter a wrong site
    pyautogui.press("backspace")
    pyautogui.press("enter")
    # wait for autofill
    sleep(3)
    # choose the first option
    pyautogui.press('down')
    pyautogui.press('enter')
    # submit the log-in form
    pyautogui.press('enter')


def open_browser():
    # open the best browser there is
    pyautogui.press('win')
    pyautogui.typewrite('brave')
    pyautogui.press('enter')
    # wait for app to open
    sleep(3)
    pyautogui.press('tab')
    pyautogui.press('space')
    # open new tab incase browser was already open
    pyautogui.hotkey('ctrl', 't')


def hvr_floor_function(value: float):
    return int(value + 0.5)


@dataclass(frozen=True, order=True)
class LoadOption:
    discount: float
    load_value: int


def calculate_ideal_load_option(current_discount: float) -> LoadOption:
    load_options = [
        LoadOption(
            discount=1 - hvr_floor_function((1 - current_discount) * load_value) / load_value,
            load_value=load_value,
        )
        for load_value in range(HEVER_MINIMUM_LOAD_VALUE, HEVER_MAXIMUM_LOAD_VALUE + 1)
    ]
    ideal_load_option = max(load_options)
    return ideal_load_option


def build_parser():
    parser = argparse.ArgumentParser(description="Auto-fill HVR payment forms using image recognition to automate"
                                                 "manual repeated low amount inputs to get "
                                                 "a higher discount percentage."
                                                 "WARNING from EULA: If you load your card more than 5 times in a day, "
                                                 "it will be frozen for 24 hours.")
    parser.add_argument("--load-count", required=True, type=int,
                        help=f"The amount of times to load. Choosing {HEVER_MAXIMUM_DAILY_LOAD_COUNT} makes it so you"
                             f"cannot use the card today anymore.")
    parser.add_argument("--current-discount-percentage", required=True, type=float,
                        help="Your current hever discount percentage. Varies with the amount already spent on the "
                             "card, during holidays and birthday months.")
    parser.add_argument(
        "--card-type",
        required=True,
        choices=["food", "standing"],
        help="Type of card to load, either the food AKA Teamim card or the standing AKA Keva card"
    )
    parser.add_argument("--card-number", required=True, type=str, help="Card number")
    parser.add_argument("--year", required=True, type=str, help="Card expiration year")
    parser.add_argument("--month", required=True, type=str, help="Card expiration month")
    parser.add_argument("--cvv", required=True, type=str, help="Card CVV")
    return parser


def main():
    args = build_parser().parse_args()

    if args.load_count > HEVER_MAXIMUM_DAILY_LOAD_COUNT:
        raise ValueError(f"The load count ({args.load_count}) cannot be greater than "
                         f"the maximum daily load count {HEVER_MAXIMUM_DAILY_LOAD_COUNT}")

    load_option = calculate_ideal_load_option(float(args.current_discount_percentage))
    print(f"Going to load the {args.card_type} card with value {load_option.load_value} "
          f"for {args.load_count} times with a discount of {load_option.discount}")

    for _ in range(args.load_count):
        open_browser()

        log_into_hever()

        load_once(args.card_type, load_option.load_value, args.card_number, args.year, args.month, args.cvv)
        # Wait to not spam the website
        sleep(60)


if __name__ == "__main__":
    main()
