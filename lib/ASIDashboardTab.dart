import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ASIDashboardTab extends StatefulWidget {
  @override
  _ASIDashboardTabState createState() => _ASIDashboardTabState();
}

class _ASIDashboardTabState extends State<ASIDashboardTab> {
  final goalCtrl = TextEditingController();
  String output = "";
  bool loading = false;

  Future<void> submitGoal() async {
    setState(() {
      loading = true;
      output = "";
    });

    final uri = Uri.parse("http://localhost:8000/asi/goal");
    final res = await http.post(
      uri,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"goal": goalCtrl.text}),
    );

    setState(() {
      loading = false;
      output = res.body;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(20),
      child: ListView(
        children: [
          Text(
            "🎯 Define a High-Level Goal",
            style: Theme.of(context).textTheme.titleLarge,
          ),
          SizedBox(height: 10),
          TextField(
            controller: goalCtrl,
            decoration: InputDecoration(labelText: "Enter your goal"),
          ),
          SizedBox(height: 10),
          ElevatedButton(
            onPressed: submitGoal,
            child: Text("Submit Goal to NARI"),
          ),
          SizedBox(height: 20),
          if (loading) CircularProgressIndicator(),
          if (output.isNotEmpty)
            SelectableText(
              output,
              style: TextStyle(fontFamily: 'monospace'),
            ),
        ],
      ),
    );
  }
}
