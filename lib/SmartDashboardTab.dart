
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SmartDashboardTab extends StatefulWidget {
  @override
  _SmartDashboardTabState createState() => _SmartDashboardTabState();
}

class _SmartDashboardTabState extends State<SmartDashboardTab> {
  final userCtrl = TextEditingController(text: "guest");
  final projectCtrl = TextEditingController();
  final featureCtrl = TextEditingController();
  final goalCtrl = TextEditingController();
  final planCtrl = TextEditingController();
  final codeCtrl = TextEditingController();
  final testCtrl = TextEditingController();

  String stack = "flutter";
  String methodology = "agile";
  bool loading = false;
  String output = "";
  String? focus;

  Future<void> fetchFocus(String prompt) async {
    final response = await http.post(
      Uri.parse("http://localhost:8000/memory_ai/consciousness/current"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"prompt": prompt}),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        focus = data["focus"];
      });
    }
  }

  Future<void> logSubconscious(String project, String feature) async {
    await http.post(
      Uri.parse("http://localhost:8000/memory_ai/subconsciousness/log"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"project": project, "feature": feature}),
    );
  }

  
  Future<void> generateSmartFeature() async {
    setState(() {
      loading = true;
      planCtrl.text = "";
      codeCtrl.text = "";
      testCtrl.text = "";
    });

    final uri = Uri.parse("http://localhost:8000/agent/run");
    final res = await http.post(uri,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "project": projectCtrl.text,
          "feature": featureCtrl.text,
          "prompt": featureCtrl.text,
          "runtime": stack
        }));

    final data = jsonDecode(res.body);
    setState(() {
      loading = false;
      planCtrl.text = data['output']?['plan'] ?? "No plan.";
      codeCtrl.text = data['output']?['code'] ?? "No code.";
      testCtrl.text = data['output']?['test'] ?? "No test.";
    });

    await logSubconscious(projectCtrl.text, featureCtrl.text);
  }


  Future<void> generateFromGoal() async {
    setState(() {
      loading = true;
      output = "";
    });

    final uri = Uri.parse("http://localhost:8000/asi/generate-features");
    final res = await http.post(uri,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "project": projectCtrl.text,
          "stack": stack,
          "methodology": methodology,
          "goal": goalCtrl.text,
          "features": goalCtrl.text
        }));

    setState(() {
      loading = false;
      output = res.body;
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: EdgeInsets.all(20),
      children: [
        if (focus != null)
          Text("🧠 Current Focus: $focus", style: TextStyle(fontWeight: FontWeight.bold)),
        TextField(controller: userCtrl, decoration: InputDecoration(labelText: "User")),
        TextField(controller: projectCtrl, decoration: InputDecoration(labelText: "Project")),
        TextField(
          controller: featureCtrl,
          decoration: InputDecoration(labelText: "Feature Description"),
          onChanged: fetchFocus,
        ),
        DropdownButton<String>(
            value: stack,
            onChanged: (val) => setState(() => stack = val ?? "flutter"),
            items: ["flutter", "react", "next", "node", "vue", "swiftui", "django"]
                .map((s) => DropdownMenuItem(value: s, child: Text(s)))
                .toList()),
        DropdownButton<String>(
            value: methodology,
            onChanged: (val) => setState(() => methodology = val ?? "agile"),
            items: ["agile", "waterfall"].map((m) => DropdownMenuItem(value: m, child: Text(m))).toList()),
        ElevatedButton(onPressed: generateSmartFeature, child: Text("⚙️ Generate Feature")),
        SizedBox(height: 20),
        TextField(controller: goalCtrl, decoration: InputDecoration(labelText: "Enter full ASI Goal list (markdown format)")),
        ElevatedButton(onPressed: generateFromGoal, child: Text("🧠 Auto Generate Features from Goal")),
        SizedBox(height: 10),
        if (loading) CircularProgressIndicator(),
        Text("🧠 Plan:", style: TextStyle(fontWeight: FontWeight.bold)),
        TextField(controller: planCtrl, maxLines: 6, decoration: InputDecoration(border: OutlineInputBorder())),
        Text("💻 Code:", style: TextStyle(fontWeight: FontWeight.bold)),
        TextField(controller: codeCtrl, maxLines: 12, decoration: InputDecoration(border: OutlineInputBorder())),
        Text("🧪 Test:", style: TextStyle(fontWeight: FontWeight.bold)),
        TextField(controller: testCtrl, maxLines: 10, decoration: InputDecoration(border: OutlineInputBorder())),
        SizedBox(height: 10),
        if (output.isNotEmpty) SelectableText(output),
      ],
    );
  }
}
