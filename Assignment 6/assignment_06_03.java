import java.util.*;
import java.util.stream.Collectors;

/**
 * Entity class representing a Student.
 * Handles individual data storage and logic for calculating personal averages.
 */
class Student {
    private int id;
    private String name;
    private List<String> courses;
    private Map<String, Integer> scores; // Stores Course Name as Key, Score as Value
    private double averageScore;

    public Student(int id, String name, List<String> courses, Map<String, Integer> scores) {
        this.id = id;
        this.name = name;
        // Defensive copying: creates a new list/map to prevent external modification
        this.courses = new ArrayList<>(courses);
        this.scores = new HashMap<>(scores);
        // Pre-calculating average at object creation to save time during later retrievals
        this.averageScore = calculateAverageScore();
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public List<String> getCourses() { return courses; }
    public Map<String, Integer> getScores() { return scores; }
    public double getAverageScore() { return averageScore; }

    /**
     * Logic: Uses Java Streams to iterate through the student's courses,
     * fetches scores from the map, and computes the mathematical mean.
     */
    private double calculateAverageScore() {
        if (courses == null || courses.isEmpty()) return 0.0;
        
        return courses.stream()
                .mapToInt(course -> scores.getOrDefault(course, 0))
                .average() // Terminal operation that returns an OptionalDouble
                .orElse(0.0);
    }

    @Override
    public String toString() {
        return String.format("Student{id=%d, name='%s', avgScore=%.2f}", id, name, averageScore);
    }
}

public class assignment_06_03 {

    /**
     * Functionality: Returns the highest performing students.
     * Logic: Sorts the stream in descending order based on averageScore and truncates to N.
     */
    public static List<Student> getTopNStudents(List<Student> students, int n) {
        return students.stream()
                .sorted(Comparator.comparingDouble(Student::getAverageScore).reversed())
                .limit(n)
                .collect(Collectors.toCollection(ArrayList::new));
    }

    /**
     * Functionality: Calculates the global average for every unique course.
     * Logic: 
     * 1. Uses a Map where the value is a double array [Total Score, Count].
     * 2. Iterates once (O(N)) to aggregate data.
     * 3. Performs a final pass to divide totals by counts.
     */
    public static Map<String, Double> getAverageScorePerCourse(List<Student> students) {
        Map<String, double[]> courseStats = new HashMap<>();

        for (Student student : students) {
            for (String course : student.getCourses()) {
                // Initialize the stats array [Sum, Count] if the course isn't in the map yet
                courseStats.putIfAbsent(course, new double[]{0.0, 0.0});
                
                double[] stats = courseStats.get(course);
                stats[0] += student.getScores().getOrDefault(course, 0); // Accumulate sum
                stats[1] += 1; // Increment count
            }
        }

        // Convert the temporary [Sum, Count] map into a final [Course, Average] map
        Map<String, Double> courseAverages = new HashMap<>();
        for (Map.Entry<String, double[]> entry : courseStats.entrySet()) {
            double totalScore = entry.getValue()[0];
            double count = entry.getValue()[1];
            courseAverages.put(entry.getKey(), totalScore / count);
        }

        return courseAverages;
    }

    /**
     * Logic: Uses 'flatMap' to drill down into the nested lists of courses across all students
     * and collects them into a Set to automatically remove duplicates.
     */
    public static Set<String> getAllUniqueCourses(List<Student> students) {
        return students.stream()
                .flatMap(s -> s.getCourses().stream()) // Flattens List<List<String>> into Stream<String>
                .collect(Collectors.toCollection(HashSet::new));
    }

    /**
     * Helper: Generates randomized mock data for testing.
     */
    private static List<Student> generateStudents(int n) {
        List<Student> students = new ArrayList<>();
        Random random = new Random();
        String[] allCourses = {"Math", "Physics", "Chemistry", "Biology", "History", "Literature", "Computer Science"};

        for (int i = 1; i <= n; i++) {
            int numCourses = random.nextInt(4) + 2; // Each student gets 2 to 5 courses
            List<String> studentCourses = new ArrayList<>();
            Map<String, Integer> studentScores = new HashMap<>();
            
            // Shuffle to assign unique random courses to each student
            List<String> availableCourses = new ArrayList<>(Arrays.asList(allCourses));
            Collections.shuffle(availableCourses, random);

            for (int j = 0; j < numCourses; j++) {
                String course = availableCourses.get(j);
                studentCourses.add(course);
                studentScores.put(course, random.nextInt(41) + 60); // Scores between 60 and 100
            }

            students.add(new Student(i, "Student_" + i, studentCourses, studentScores));
        }
        return students;
    }

    /**
     * Performance Analysis:
     * This main method executes the logic across different sample sizes.
     * It uses System.nanoTime() to measure execution speed in milliseconds.
     */
    public static void main(String[] args) {
        int[] sampleSizes = {10, 100, 1000, 10000};

        for (int n : sampleSizes) {
            System.out.println("--- Testing with n = " + n + " students ---");
            List<Student> students = generateStudents(n);

            // Test 1: Sorting and Filtering (O(N log N))
            long startTime = System.nanoTime();
            getTopNStudents(students, Math.min(5, n));
            long endTime = System.nanoTime();
            System.out.printf("Top N Students Time: %.4f ms%n", (endTime - startTime) / 1_000_000.0);

            // Test 2: Aggregation and Map manipulation (O(N))
            startTime = System.nanoTime();
            getAverageScorePerCourse(students);
            endTime = System.nanoTime();
            System.out.printf("Average Score Per Course Time: %.4f ms%n", (endTime - startTime) / 1_000_000.0);

            // Test 3: Set uniqueness (O(N))
            startTime = System.nanoTime();
            getAllUniqueCourses(students);
            endTime = System.nanoTime();
            System.out.printf("Unique Courses Time: %.4f ms%n%n", (endTime - startTime) / 1_000_000.0);
        }
    }
}