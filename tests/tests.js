/*
Tests to run in the Chrome console
*/

// Test 01 Flesch-Kincaid Grade Level
// Expect: {grade: "10.77", message: "OK", status: "OK"}
fetch('http://localhost:5000/fkgl', {
  method: 'POST',
  body: "We live in strange times. All evidence shows we’re driving ourselves to a climate breakdown that threatens our survival, and what do governments do? Do they employ the many available solutions and work to educate the public and resolve the crisis? A few are trying, while some outright deny the evidence, some attack citizens who speak out about the emergency and others claim to care while planning ways to sell enough fossil fuels to cook the planet.",
  headers: {
    'Content-type': 'text/plain; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)

// Test 02 Flesch Reading Ease Score
// Expect: {message: "OK", score: "52.16", status: "OK"}
fetch('http://localhost:5000/fres', {
  method: 'POST',
  body: "We live in strange times. All evidence shows we’re driving ourselves to a climate breakdown that threatens our survival, and what do governments do? Do they employ the many available solutions and work to educate the public and resolve the crisis? A few are trying, while some outright deny the evidence, some attack citizens who speak out about the emergency and others claim to care while planning ways to sell enough fossil fuels to cook the planet.",
  headers: {
    'Content-type': 'text/plain; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)

// Test 03 Word Count
// Expect: {count: "77", message: "OK", status: "OK"}
fetch('http://localhost:5000/word-count', {
  method: 'POST',
  body: "We live in strange times. All evidence shows we’re driving ourselves to a climate breakdown that threatens our survival, and what do governments do? Do they employ the many available solutions and work to educate the public and resolve the crisis? A few are trying, while some outright deny the evidence, some attack citizens who speak out about the emergency and others claim to care while planning ways to sell enough fossil fuels to cook the planet.",
  headers: {
    'Content-type': 'text/plain; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)

