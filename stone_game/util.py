def take_input_int(text, error, valid_ints):
  """
  Take integer input
  text: prompt text
  error: what prints if the text is not in valid_ints
  valid_ints: an array of integers which are acceptable input
  """
  try:
    inp = int(input(text))
    if inp in valid_ints:
      return (inp)
    raise NameError(error)
  except NameError:
    print(error)
  except ValueError:
    print('Thats not a number')

  return take_input_int(text, error, valid_ints)

def take_input_str(text, error, valid_choices):
  """
  Take input from a list of valid choices
  text: prompt text
  error: what prints if the text is not in valid_choices
  valid_choices: an array of values to select
  """
  try:
    inp = input(text).strip()
    if len(inp) == 0:
      raise ValueError('No input')
    if valid_choices is None or inp.lower() in valid_choices:
      return (inp)
    raise NameError(error)
  except NameError:
    if error is not None:
      print(error)
    elif len(valid_choices):
      print('Invalid choice, your choices are: ', valid_choices)
  except ValueError:
    print('Empty input.')

  return take_input_str(text, error, valid_choices)
