#include <stdio.h>

/* Simple error codes */
#define OK 0
#define ERROR 1

/* global buffer for input data
 * get INPUT_BUFFER from size of file
 * if READ_STDIN is 0 then read from file named "input.txt"
 */
#define READ_STDIN 1
#define INPUT_BUFFER 1000
char source[INPUT_BUFFER + 1];

/* Read input */
int read_input()
{
  const char *name;
  FILE *fp;

  if (READ_STDIN == 1)
  {
    name = "stdin";
    fp = stdin;
  }
  else
  {
    name = "input.txt";
    fp = fopen(name, "r");
  }
  if (fp != NULL)
  {
    size_t newLen = fread(source, sizeof(char), INPUT_BUFFER, fp);
    if (ferror(fp) != 0)
    {
      fprintf(stderr, "Error reading %s\n", name);
      return ferror(fp);
    }
    else
    {
      source[newLen++] = '\0'; /* Just to be safe. */
    }

    fclose(fp);
    return OK;
  }
  else
  {
    fprintf(stderr, "Error opening %s\n", name);
    return ERROR;
  }
}

#define LEFT 'L'
#define RIGHT 'R'
#define NORTH 1
#define EAST 2
#define SOUTH 3
#define WEST 4

struct Location
{
  int x; /* distance moved horizontally */
  int y; /* distance moved vertically */
};

struct Location move(struct Location location, int orientation, int distance)
{
  switch (orientation)
  {
  case NORTH:
    location.y += distance;
    break;
  case EAST:
    location.x += distance;
    break;
  case SOUTH:
    location.y -= distance;
    break;
  case WEST:
    location.x -= distance;
    break;
  default:
    break;
  }
  return location;
}

/* Manhattan distance of location from (0,0) */
int manhattan(struct Location location)
{
  int x = (location.x < 0 ? -location.x : location.x);
  int y = (location.y < 0 ? -location.y : location.y);
  return x + y;
}

int parse()
{
  int i = 0;                         /* index into input buffer*/
  char c;                            /* current character being parsed*/
  int distance = 0;                  /* value being parsed that we should travel in the current move*/
  int direction = 0;                 /* direction to turn; 0 => is not defined and we are not ready to parse a number*/
  int orientation = 1;               /* direction we are headed NORTH..WEST*/
  struct Location location = {0, 0}; /* current location */

  while ((c = source[i++]) != '\0')
  {
    // printf("char: '%c'\n", c);
    switch (c)
    {
    case LEFT:
      orientation -= 1;
      if (orientation < NORTH)
      {
        orientation = WEST;
      }
      distance = 0;
      break;
    case RIGHT:
      orientation += 1;
      if (orientation > WEST)
      {
        orientation = NORTH;
      }
      distance = 0;
      break;
    case '0' ... '9': /* GCC and clang extension to C */
      distance = distance * 10 + (c - '0');
      break;
    case ',':
      /* we are done parsing a distance and orientation is set, so move */
      // printf("move: from:(%d,%d), orientation:%d, distance:%d\n", location.x, location.y, orientation, distance);
      location = move(location, orientation, distance);
      /* set the distance to zero so we do not make this move again (i.e. at EOF) */
      distance = 0;
      break;
    default:
      /* ignore spaces and any other characters*/
      break;
    }
  }
  /* there is no trailing comma, just an EOF, so add the final move*/
  if (distance > 0)
  {
    // printf("move: from:(%d,%d), orientation:%d, distance:%d\n", location.x, location.y, orientation, distance);
    location = move(location, orientation, distance);
  }
  return manhattan(location);
}

int main()
{
  int status = read_input();
  if (status == OK)
  {
    // fputs(source, stdout);
    int len = parse();
    printf("Part 1: %d\n", len);
    return OK;
  }
  return status;
}
