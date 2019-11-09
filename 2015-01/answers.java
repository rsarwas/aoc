import java.io.IOException;

class AOC {
    public static void main(String[] args)
        throws IOException
    {
        int floor = 0;
        int basement = -1;
        int position = 0;
        int ch;
        while ((ch = System.in.read()) != -1)
        {
            floor +=  (ch == '(') ? 1 : (ch == ')') ? -1: 0;
            position++;
            if (floor == -1 && basement == -1) {
                basement = position;
            }
        }
	    System.out.println("Part 1: " + floor);
	    System.out.println("Part 2: " + basement);
    }
}
