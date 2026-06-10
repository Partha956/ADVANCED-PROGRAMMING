import React, { useState, type FormEvent } from 'react';

// 1. DATA MODELING
// Using a Type alias to define the shape of a Student object.
// We use a Set for 'enrolledCourses' to ensure a student cannot be added to the same course twice.
type Student = {
  id: number;
  name: string;
  enrolledCourses: Set<string>;
  gpa: number;
};

export default function App() {
  // 2. STATE MANAGEMENT
  // We use a Map to store students (ID -> Student Object).
  // Maps are excellent for performance when adding/removing items by a unique key.
  const [students, setStudents] = useState<Map<number, Student>>(new Map());
  
  // Controlled Input States: These track what the user types in real-time.
  const [name, setName] = useState<string>('');
  const [coursesInput, setCoursesInput] = useState<string>('');
  const [gpa, setGpa] = useState<string>('');
  const [filterCourse, setFilterCourse] = useState<string>('');

  // 3. LOGIC: ADDING A STUDENT
  const handleAddStudent = (e: FormEvent) => {
    e.preventDefault(); // Prevents the browser from refreshing the page
    const id = Date.now(); // Using timestamp as a simple unique ID
    
    // Transform the comma-separated string into a Set of clean strings
    const coursesSet = new Set(
      coursesInput
        .split(',')           // Split by comma
        .map((c) => c.trim()) // Remove extra whitespace
        .filter((c) => c.length > 0) // Remove empty strings
    );

    const newStudent: Student = {
      id,
      name,
      enrolledCourses: coursesSet,
      gpa: parseFloat(gpa) || 0, // Convert string input to number
    };

    // IMMUTABILITY: To update state in React, we must provide a NEW Map.
    // We spread the previous map and add the new student entry.
    setStudents((prev) => new Map([...prev, [id, newStudent]]));
    
    // Clear form inputs after successful submission
    setName('');
    setCoursesInput('');
    setGpa('');
  };

  // 4. LOGIC: REMOVING A STUDENT
  const handleRemoveStudent = (id: number) => {
    setStudents((prev) => {
      // Create a shallow copy of the Map to maintain immutability
      const newStudentsMap = new Map([...prev]);
      newStudentsMap.delete(id); // Delete by ID
      return newStudentsMap;     // Return the new map to trigger a re-render
    });
  };

  // 5. DERIVED STATE: CALCULATING ALL UNIQUE COURSES
  // This calculates a list of every course offered across all students.
  // We do this during the render phase so it's always up to date.
  const uniqueCoursesSet = Array.from(students.values()).reduce((acc, student) => {
    // Merge the current student's courses into the accumulator Set
    return new Set([...acc, ...student.enrolledCourses]);
  }, new Set<string>());

  const uniqueCoursesList = Array.from(uniqueCoursesSet);

  // 6. DERIVED STATE: FILTERING AND SORTING
  // Instead of storing "filtered students" in state, we calculate them on the fly.
  const displayedStudents = Array.from(students.values())
    // Step A: Filter by course (if a filter is selected)
    .filter((student) => 
      filterCourse ? student.enrolledCourses.has(filterCourse) : true
    )
    // Step B: Sort by GPA (highest to lowest)
    .sort((a, b) => b.gpa - a.gpa); 

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h1>Course Enrollment Dashboard</h1>

      {/* FORM SECTION */}
      <section style={{ marginBottom: '2rem', padding: '1rem', border: '1px solid #ccc' }}>
        <h2>Add Student</h2>
        <form onSubmit={handleAddStudent} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Courses (comma separated)"
            value={coursesInput}
            onChange={(e) => setCoursesInput(e.target.value)}
            required
          />
          <input
            type="number"
            step="0.1"
            max="4.0"
            min="0"
            placeholder="GPA"
            value={gpa}
            onChange={(e) => setGpa(e.target.value)}
            required
          />
          <button type="submit">Add Student</button>
        </form>
      </section>

      {/* GLOBAL COURSE LIST SECTION */}
      <section style={{ marginBottom: '2rem' }}>
        <h2>All Offered Courses</h2>
        <p>
          {uniqueCoursesList.length > 0 
            ? uniqueCoursesList.map((course) => (
                <span key={course} style={{ marginRight: '10px', background: '#e5e7eb', padding: '4px 8px', borderRadius: '4px' }}>
                  {course}
                </span>
              ))
            : "No courses enrolled yet."}
        </p>
      </section>

      {/* STUDENT TABLE SECTION */}
      <section>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2>Enrolled Students</h2>
          
          {/* FILTER DROPDOWN */}
          <select 
            value={filterCourse} 
            onChange={(e) => setFilterCourse(e.target.value)}
          >
            <option value="">All Courses</option>
            {uniqueCoursesList.map((course) => (
              <option key={course} value={course}>
                Filter by: {course}
              </option>
            ))}
          </select>
        </div>

        {/* CONDITIONAL RENDERING: Show message if no students found */}
        {displayedStudents.length === 0 ? (
          <p>No students match your criteria.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '2px solid #ccc' }}>
                <th style={{ padding: '8px' }}>Name</th>
                <th style={{ padding: '8px' }}>GPA</th>
                <th style={{ padding: '8px' }}>Courses</th>
                <th style={{ padding: '8px' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {displayedStudents.map((student) => (
                <tr key={student.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '8px' }}>{student.name}</td>
                  <td style={{ padding: '8px' }}>{student.gpa.toFixed(2)}</td>
                  {/* Convert the Set of courses back to a string for display */}
                  <td style={{ padding: '8px' }}>{Array.from(student.enrolledCourses).join(', ')}</td>
                  <td style={{ padding: '8px' }}>
                    <button onClick={() => handleRemoveStudent(student.id)}>
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}