# Time Tracker Discord Bot

![License](https://img.shields.io/github/license/Raffiesaurus/time-tracker)
![Last Commit](https://img.shields.io/github/last-commit/Raffiesaurus/time-tracker)

A Discord bot for tracking user time zones and checking the local time of other users in a server.

## Features

- Set and store time zones for users.
- Retrieve the current time of a mentioned user.
- List recent time zone additions.
- Uses IANA time zone codes for accuracy.

## Bot Commands

- `!setTZ <timezone> <country>` - Set your timezone. Use an IANA time zone code like `Europe/London` or `America/New_York`.
  - **Example:** `!setTZ Europe/London Scotland`
- `!time @user` - Get the current time of the mentioned user.
- `!list <number>` - Get the last `<number>` of people times added.
- **Time Zone List:** For a full list of IANA time zones, visit [this link](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

## Installation

To set up and run the bot, follow these steps:

### Prerequisites

- Python 3.8+
- A Discord bot token (from the [Discord Developer Portal](https://discord.com/developers/applications))
- Required dependencies (install using the command below)

### Clone the Repository

```sh
git clone https://github.com/Raffiesaurus/time-tracker.git
cd time-tracker
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Run the Bot

```sh
python bot.py
```

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback, reach out to me via [LinkedIn](https://www.linkedin.com/in/raffiesaurus) or check out my [portfolio](https://raffiesaurus.com/).
