I will write a simple Python bot for you that fixes text inputs, changing them from "yes" to "Yes". This ensures the correct capitalization. The bot will take a string data and format it correctly.

```python
class FormatterAgent:

    def __init__(self):
        pass

    def fix_format(self, input_text):
        """
        This function fixes the format of the 'yes' text, replacing it with 'Yes'
        """
        output_text = input_text.replace('yes', 'Yes')
        return output_text


if __name__ == '__main__':
    bot = FormatterAgent()
    print(bot.fix_format("yes, it's true. yes, it's correct."))
```

When you execute this script, it will correct the format of the text, replacing 'yes' with 'Yes'. So, instances of the word 'yes' will be turned into 'Yes'.