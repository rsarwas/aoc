import java.util.Scanner;

class AOC {
    public static void main(String[] args) {
        int total_paper = 0;
        int total_ribbon = 0;
        Scanner scan = new Scanner(System.in);
        while (scan.hasNextLine()) {
            String line = scan.nextLine();
            String[] dims = line.split("x");
            int h = Integer.parseInt(dims[0]);
            int w = Integer.parseInt(dims[1]);
            int l = Integer.parseInt(dims[2]);
            Present p = new Present(h, w, l);
            total_paper += p.paper();
            total_ribbon += p.ribbon();
        }
        scan.close();
	    System.out.println("Part 1: " + total_paper);
	    System.out.println("Part 2: " + total_ribbon);
    }
}

final class Present {
    private int width = 0, length = 0, height = 0;

    public Present(int height, int width, int length)
    {
        this.length = length;
        this.width = width;
        this.height = height;
    }

    private int min3(int a, int b, int c)
    {
        int d = (a < b) ? a : b;
        return (d < c) ? d : c;
    }

    private int smallestSidePerimeter() {
        return this.min3(
            2*this.length + 2*this.width,
            2*this.width + 2*this.height,
            2*this.height + 2*this.length
        );
    }

    private int smallestSideArea() {
        return this.min3(
            this.length*this.width,
            this.width*this.height,
            this.height*this.length
        );
    }

    private int surfaceArea() {
        return 2*this.length*this.width + 
                2*this.width*this.height +
                2*this.height*this.length;
    }

    private int volume() {
        return this.length * this.width * this.height;
    }

    public int paper() {
        return this.surfaceArea() + this.smallestSideArea();
    }

    public int ribbon() {
        return this.volume() + this.smallestSidePerimeter();
    }
}
