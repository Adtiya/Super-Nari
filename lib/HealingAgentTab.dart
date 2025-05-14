
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class HealingAgentTab extends StatefulWidget {
  @override
  _HealingAgentTabState createState() => _HealingAgentTabState();
}

class _HealingAgentTabState extends State<HealingAgentTab> {
  final TextEditingController promptCtrl = TextEditingController();
  bool loading = false;
  List<dynamic> steps = [];
  String status = "";

  Future<void> runSelfHealingAgent() async {
    setState(() {
      loading = true;
      steps = [];
      status = "";
    });

    final uri = Uri.parse("http://localhost:8000/agent/self-heal");
    final response = await http.post(uri,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"prompt": promptCtrl.text}),
    );

    if (response.statusCode == 200) {
      final json = jsonDecode(response.body);
      setState(() {
        status = json["status"];
        steps = json["steps"];
      });
    } else {
      setState(() {
        status = "error";
        steps = [{"attempt": 0, "error": "Server error: ${response.statusCode}"}];
      });
    }

    setState(() {
      loading = false;
    });
  }

  Widget buildStepCard(Map step) {
    return Card(
      margin: EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Attempt ${step["attempt"]}", style: TextStyle(fontWeight: FontWeight.bold)),
            if (step["success"] == true) Text("✅ Success", style: TextStyle(color: Colors.green)),
            if (step["success"] == false) Text("❌ Failed", style: TextStyle(color: Colors.red)),
            if (step["output"] != null) Text("Output: ${step["output"]}", style: TextStyle(fontFamily: 'monospace')),
            if (step["error"] != null) Text("Error: ${step["error"]}", style: TextStyle(fontFamily: 'monospace', color: Colors.red)),
            SizedBox(height: 8),
            Text("Generated Code:", style: TextStyle(fontWeight: FontWeight.bold)),
            Container(
              width: double.infinity,
              padding: EdgeInsets.all(8),
              color: Colors.grey.shade900,
              child: Text(step["code"] ?? "", style: TextStyle(fontFamily: 'monospace', color: Colors.white)),
            )
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(20),
      child: ListView(
        children: [
          Text("🔁 Self-Healing Agent", style: Theme.of(context).textTheme.headlineSmall),
          TextField(
            controller: promptCtrl,
            decoration: InputDecoration(labelText: "Enter your agent task (e.g., summarize news, scrape site)"),
          ),
          SizedBox(height: 10),
          ElevatedButton(
            onPressed: loading ? null : runSelfHealingAgent,
            child: Text("Run Agent"),
          ),
          if (loading) Center(child: CircularProgressIndicator()),
          if (status.isNotEmpty) Text("Status: $status", style: TextStyle(fontWeight: FontWeight.bold)),
          SizedBox(height: 20),
          ...steps.map((step) => buildStepCard(step)).toList(),
        ],
      ),
    );
  }
}
