def take_input_int(text, error, valid_ints):
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
  try:
    inp = input(text).strip()
    if valid_choices is None or inp.lower() in valid_choices:
      return (inp)
    raise NameError(error)
  except NameError:
    if error is not None:
      print(error)
  
  return take_input_str(text, error, valid_choices)
