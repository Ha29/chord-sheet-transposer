transpose_num = input("Transpose by how much? (positive number), 11 is -1, 10 is -2, etc.:\n")
if not transpose_num.isnumeric():
  raise Exception("Need positive numeric input")

input_file_name = input("What is your filename (default: myfile.txt) (Only alphanumeric a-zA-Z0-9)?\n")

cleaned_file_name = ''.join(c for c in input_file_name.split('.')[0] if c.isalnum())

if input_file_name == '':
  input_file_name = 'myfile.txt'
elif len(input_file_name.split('.')) > 1:
  ext = input_file_name.split('.')[-1]

# Using readlines()
file1 = open(input_file_name, 'r')
fileLines = file1.readlines()

# 0 - 11 are the indices, mod 12 the transpose num
notes_array = 'C Db D Eb E F Gb G Ab A Bb B'.split(' ')
notes_dict = {}
for idx, note in enumerate(notes_array):
  notes_dict[idx] = note
  notes_dict[note] = idx 
notes_dict['C#'] = 1
notes_dict['D#'] = 3
notes_dict['F#'] = 6
notes_dict['G#'] = 8
notes_dict['A#'] = 10

music_key = input("What is the key of the song? (default: C) (Use major key and only the letter and sharp or flat, don't put C major, C# or Db is okay)\n")
if music_key not in notes_dict:
  print('Invalid music key, using C\n')
  music_key = 'C'  
new_transpose_key = notes_dict[music_key] + int(transpose_num) % 12
new_key = notes_dict[new_transpose_key]

use_flat = False
if 'b' in new_key:
  use_flat = True

def get_correct_sharp_flat_note(note, use_flat=False):
  if use_flat:
    return note
  if note in notes_dict and 'b' in note:
    if note == 'Db':
      return 'C#'
    elif note == 'Eb':
      return 'D#'
    elif note == 'Gb':
      return 'F#'
    elif note == 'Bb':
      return 'A#'
  return note

#counts spaces up until a string match
def space_counter(string, string_to_match):
  count = 0
  match_idx = 0
  for char in string:
    if char == ' ':
      count += 1
    elif char == string_to_match[match_idx]:
      match_idx += 1
      count += 1
    else:
      match_idx = 0
      count = 0
  return count

#figure out how to count the spaces in each of the lines you want to replace 
#figure out how to handle / bass 

def valid_chord(chord):
  return len(chord) >= 1 and chord[0] in notes_dict

# Strips the newline character

def find_main_chord(Lines, transpose_num):
  new_lines = []
  for line in Lines:
    transcribed_line = ''
    if '|' in line: 
      curr_line = line.split(' ')
      for chord in curr_line:
        # print('chord: ', chord)
        if chord == '':
          transcribed_line += ' '
          continue
        elif chord == '|' or not valid_chord(chord):
          transcribed_line += chord + ' '
          continue
        has_sharp_flat = False
        if len(chord) >= 1 and chord != '|':
          chord_note = chord[0]
          if len(chord) > 1 and (chord[1] == '#' or chord[1] == 'b'):
            chord_note += chord[1]
            has_sharp_flat = True
          elif len(chord) == 1:
            chord_note = chord[0]
          try:
            note_idx = notes_dict[chord_note]
            note_idx = (note_idx + transpose_num) % 12
            new_note = get_correct_sharp_flat_note(notes_dict[note_idx], use_flat)
            if has_sharp_flat:
              new_note = notes_dict[note_idx] + chord[2:]
            else:
              new_note = notes_dict[note_idx] + chord[1:]
            transcribed_line += new_note
          except KeyError:
            print('note does not exist: ', chord_note)
            continue
      new_lines += [transcribed_line]
    else:
      new_lines += [line]
  return new_lines

def find_slash_notes(Lines, transpose_num):
  transcribed_lines = []
  for line in Lines:
    transcribed_line = ''
    if '|' in line:
      idx = 0
      while idx < len(line):
        char = line[idx]
        try:
          if char == '/' and idx + 2 <= len(line) - 1:
            # print('linehere: ', line)
            if line[idx + 1] in notes_dict and line[idx + 2] in ['b', '#']:
              note_idx = notes_dict[line[idx + 1] + line[idx + 2]]
              note_idx = (note_idx + transpose_num) % 12
              transcribed_line += '/' + get_correct_sharp_flat_note(notes_dict[note_idx], use_flat)
              idx += 3
              continue
            elif line[idx + 1] in notes_dict:
              note_idx = notes_dict[line[idx + 1]]
              note_idx = (note_idx + transpose_num) % 12
              transcribed_line += '/' + get_correct_sharp_flat_note(notes_dict[note_idx], use_flat)
              idx += 2
              continue
            else:
              print('Warning at: ', line[idx + 1])
          elif char == '/' and idx + 1 <= len(line) - 1:
            if line[idx + 1] in notes_dict:
              note_idx = notes_dict[line[idx + 1]]
              note_idx = (note_idx + transpose_num) % 12
              transcribed_line += '/' + get_correct_sharp_flat_note(notes_dict[note_idx], use_flat)
              idx += 2
              continue
            else:
              print('Warning at: ', line[idx + 1])
        except KeyError:
          print('note does not exist: ', chord_note)
        transcribed_line += char
        idx += 1
    else:
      transcribed_line = line
    transcribed_lines += [transcribed_line]
  return transcribed_lines
        


# transpose_num = 2
new_lines = find_main_chord(fileLines, int(transpose_num))
new_lines = find_slash_notes(new_lines, int(transpose_num))
  # print(new_lines)

file2 = open(input_file_name.split('.')[0] + '_transposedtoKeyOf' + str(new_key) + '.txt', 'w+')
file2.writelines(new_lines)
print('outputted at ', input_file_name.split('.')[0] + '_transposedtoKeyOf' + str(new_key) + '.txt')
