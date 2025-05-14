
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class FeatureTab extends StatefulWidget {
  @override
  _FeatureTabState createState() => _FeatureTabState();
}

class _FeatureTabState extends State<FeatureTab> {
  final userCtrl = TextEditingController(text: "guest");
  final projectCtrl = TextEditingController();
  final featureCtrl = TextEditingController();
  String stack = "flutter";
  String methodology = "agile";
  String output = "";

  @override
  void dispose() {
    userCtrl.dispose();
    projectCtrl.dispose();
    featureCtrl.dispose();
    super.dispose();
  }

  Future<void> buildFeature() async {
    final uri = Uri.parse("http://localhost:8000/agent/run");
    final res = await http.post(uri,
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": "supersecret"
        },
        body: jsonEncode({
          "user": userCtrl.text,
          "project": projectCtrl.text,
          "feature": featureCtrl.text,
          "agents": ["planner", "dev", "test"],
          "methodology": methodology,
          "action": "add",
          "target": stack,
          "input_mode": "story"
        }));

    final data = jsonDecode(res.body);
    setState(() {
      output = "🧠 ${data['focus']}\n"
               "🔄 Flow: ${data['agents'].join(' → ')}\n"
               "✅ Plan: ${data['output']['plan']}\n\n"
               "🛠 Code: ${data['output']['code']?.substring(0, 200)}...\n\n"
               "🧪 Test: ${data['output']['test']?.substring(0, 200)}...";
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: EdgeInsets.all(20),
      children: [
        TextField(controller: userCtrl, decoration: InputDecoration(labelText: "User")),
        TextField(controller: projectCtrl, decoration: InputDecoration(labelText: "Project")),
        TextField(controller: featureCtrl, decoration: InputDecoration(labelText: "Feature Description")),
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
        ElevatedButton(onPressed: buildFeature, child: Text("Build Feature")),
        SizedBox(height: 10),
        SelectableText(output),
      ],
    );
  }
}
