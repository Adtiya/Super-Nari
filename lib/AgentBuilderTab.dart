
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AgentBuilderTab extends StatefulWidget {
  @override
  _AgentBuilderTabState createState() => _AgentBuilderTabState();
}

class _AgentBuilderTabState extends State<AgentBuilderTab> {
  final userCtrl = TextEditingController(text: "super_agent_user");
  final projectCtrl = TextEditingController(text: "agents");
  final featureCtrl = TextEditingController();
  final planCtrl = TextEditingController();
  final codeCtrl = TextEditingController();
  final testCtrl = TextEditingController();

  String output = "";
  bool loading = false;

  Future<void> generateAgent() async {
    setState(() {
      loading = true;
      output = "";
      planCtrl.clear();
      codeCtrl.clear();
      testCtrl.clear();
    });

    final uri = Uri.parse("http://localhost:8000/agent/run");
    final res = await http.post(uri,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "user": userCtrl.text,
        "project": projectCtrl.text,
        "feature": featureCtrl.text,
        "agents": ["planner", "dev", "test"],
        "methodology": "agile",
        "action": "add",
        "target": "python",
        "input_mode": "story"
      }));

    final data = jsonDecode(res.body);
    setState(() {
      loading = false;
      planCtrl.text = data['output']['plan']['plan'] ?? "No plan.";
      codeCtrl.text = data['output']['code']['code'] ?? "No code.";
      testCtrl.text = data['output']['test']['test'] ?? "No test.";
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: EdgeInsets.all(20),
      children: [
        Text("🧠 Build a Python AI Agent", style: Theme.of(context).textTheme.titleLarge),
        TextField(controller: featureCtrl, decoration: InputDecoration(labelText: "Describe the AI agent you want")),
        SizedBox(height: 10),
        ElevatedButton(onPressed: generateAgent, child: Text("⚙️ Generate Agent")),
        if (loading) ...[
          SizedBox(height: 10),
          CircularProgressIndicator(),
        ],
        if (!loading && planCtrl.text.isNotEmpty) ...[
          SizedBox(height: 20),
          Text("📝 Plan"),
          TextField(controller: planCtrl, maxLines: 5, decoration: InputDecoration(border: OutlineInputBorder())),
          SizedBox(height: 10),
          Text("💻 Code"),
          TextField(controller: codeCtrl, maxLines: 14, decoration: InputDecoration(border: OutlineInputBorder())),
          SizedBox(height: 10),
          Text("🧪 Test"),
          TextField(controller: testCtrl, maxLines: 8, decoration: InputDecoration(border: OutlineInputBorder())),
        ]
      ],
    );
  }
}
