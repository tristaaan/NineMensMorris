

def take_input(text, error, valid_ints):
  try:
    inp = int(input(text))
    if inp in valid_ints:
      return (inp)
    raise NameError(error)
  except NameError:
    print(error)
  except ValueError:
    print('Thats not a number')

  return take_input(text, error, valid_ints)
