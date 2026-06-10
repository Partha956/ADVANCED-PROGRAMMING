import java.util.*;

public class ArrayListBookSearch {
    public static void main(String[] args) {
        ArrayList<String> books = new ArrayList<>();
        Scanner sc = new Scanner(System.in);

        books.add("Rich dad Poor dad");
        books.add( "Money and Muscle Power");
        books.add( "Buffalo Nationalism in Indian politics");
        books.add( "Atomic Habits");
        books.add( "Start with Why");
        

        System.out.println( "Enter the word toe search");
        String searchWord = sc.nextLine();

        boolean found = false;

        for(String book : books) {
            if (book.toLowerCase().contains(searchWord.toLowerCase())) {
                System.out.println("Found" + book);
                found = true;
            }
        }

        if (!found) {
            System.out.println("No book title found having the word you entered!");
        }

        sc.close();
        
    }
}