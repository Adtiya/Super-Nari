
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SuperAgentBuilderTab extends StatefulWidget {
  @override
  _SuperAgentBuilderTabState createState() => _SuperAgentBuilderTabState();
}

class _SuperAgentBuilderTabState extends State<SuperAgentBuilderTab> {

Future<void> runScript(String code, String lang) async {
  final uri = Uri.parse("http://localhost:8000/agent/run-script");

  final response = await http.post(
    uri,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({
      "language": lang,
      "code": code
    }),
  );

  if (response.statusCode == 200) {
    final result = jsonDecode(response.body);
    print("✅ Output: ${result['output']}");
    print("⚠️ Error (if any): ${result['error']}");
  } else {
    print("❌ Script run failed: ${response.statusCode} ${response.body}");
  }
}

  final userCtrl = TextEditingController(text: "complex_agent_user");
  final projectCtrl = TextEditingController(text: "super_agents");
  final featureCtrl = TextEditingController();
  final planCtrl = TextEditingController();
  final codeCtrl = TextEditingController();
  final testCtrl = TextEditingController();

  String output = "";
  String runOutput = "";
  bool loading = false;
  bool running = false;

  Future<void> generateSuperAgent() async {
    setState(() {
      loading = true;
      output = "";
      runOutput = "";
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

  Future<void> runAgentScript() async {
    setState(() {
      running = true;
      runOutput = "";
    });

    final uri = Uri.parse("http://localhost:8000/agent/run-script");
    final res = await http.post(uri,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "project": projectCtrl.text,
        "feature": featureCtrl.text,
      }));

    final result = jsonDecode(res.body);
    setState(() {
      running = false;
      runOutput = (result['stdout'] ?? '') + (result['stderr'] ?? '');
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: EdgeInsets.all(20),
      children: [
          SizedBox(height: 20),
          if (runOutput.isNotEmpty) ...[
            Text("🖥 Output:", style: TextStyle(fontWeight: FontWeight.bold)),
            Container(
              padding: EdgeInsets.all(10),
              margin: EdgeInsets.symmetric(vertical: 5),
              decoration: BoxDecoration(
                color: Colors.black87,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(runOutput, style: TextStyle(color: Colors.white, fontFamily: 'monospace')),
            ),
          ],

        Text("🧠 Build a Super Complex AI Agent", style: Theme.of(context).textTheme.titleLarge),
        TextField(controller: featureCtrl, decoration: InputDecoration(labelText: "Describe your multi-agent system")),
        SizedBox(height: 10),
        ElevatedButton(onPressed: generateSuperAgent, child: Text("🚀 Generate Super Agent")),
        if (loading) ...[
          SizedBox(height: 10),
          CircularProgressIndicator(),
        ],
        if (!loading && planCtrl.text.isNotEmpty) ...[
          SizedBox(height: 20),
          Text("📝 Plan"),
          TextField(controller: planCtrl, maxLines: 6, decoration: InputDecoration(border: OutlineInputBorder())),
          SizedBox(height: 10),
          Text("💻 Code"),
          TextField(controller: codeCtrl, maxLines: 14, decoration: InputDecoration(border: OutlineInputBorder())),
          SizedBox(height: 10),
          Text("🧪 Test"),
          TextField(controller: testCtrl, maxLines: 8, decoration: InputDecoration(border: OutlineInputBorder())),
          SizedBox(height: 10),
          ElevatedButton(onPressed: runAgentScript, child: Text("▶ Run Agent")),
          if (running) CircularProgressIndicator(),
          if (runOutput.isNotEmpty)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("📤 Agent Output:", style: TextStyle(fontWeight: FontWeight.bold)),
                SelectableText(runOutput, style: TextStyle(fontFamily: 'monospace'))
              ],
            )
        ]
      ],
    );
  }
}
