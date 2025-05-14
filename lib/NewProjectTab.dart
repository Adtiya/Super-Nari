
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class NewProjectTab extends StatefulWidget {
  @override
  _NewProjectTabState createState() => _NewProjectTabState();
}

class _NewProjectTabState extends State<NewProjectTab> {
  String selectedLanguage = "python";  // Default to Python

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: EdgeInsets.all(20),
      children: [
        // Other New Project fields
        DropdownButton<String>(
          value: selectedLanguage,
          onChanged: (String? newValue) {
            setState(() {
              selectedLanguage = newValue!;
            });
          },
          items: <String>['python', 'node', 'go', 'java', 'rust', 'bash', 'swift']
              .map<DropdownMenuItem<String>>((String value) {
            return DropdownMenuItem<String>(
              value: value,
              child: Text(value.toUpperCase()),
            );
          }).toList(),
        ),
        ElevatedButton(
          onPressed: () async {
            final uri = Uri.parse("http://localhost:8000/agent/run");
            final res = await http.post(uri,
                headers: {"Content-Type": "application/json"},
                body: jsonEncode({
                  "user": "user_name",  // Customize user_name or get it dynamically
                  "project": "project_name",  // Customize project_name
                  "feature": "agent_feature",
                  "agents": ["planner", "dev", "test"],
                  "methodology": "agile",
                  "target": selectedLanguage,  // Pass the selected language here
                  "input_mode": "story",
                }));

            // Handle the backend response and display the results
            final data = jsonDecode(res.body);
            // Update UI with generated code and plan
          },
          child: Text("Generate Agent in $selectedLanguage"),
        ),
      ],
    );
  }
}
