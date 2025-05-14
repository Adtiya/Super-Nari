
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class DeployTab extends StatefulWidget {
  @override
  _DeployTabState createState() => _DeployTabState();
}

class _DeployTabState extends State<DeployTab> {
  final userCtrl = TextEditingController(text: "guest");
  final projectCtrl = TextEditingController();
  final messageCtrl = TextEditingController(text: "🚀 Commit from Super NARI UI");
  final tokenCtrl = TextEditingController();
  final repoUrlCtrl = TextEditingController();
  String output = "";
  Map<String, dynamic> memoryPreview = {};

  @override
  void dispose() {
    userCtrl.dispose();
    projectCtrl.dispose();
    messageCtrl.dispose();
    tokenCtrl.dispose();
    repoUrlCtrl.dispose();
    super.dispose();
  }

  Future<void> fetchMemoryPreview() async {
    final uri = Uri.parse("http://localhost:8000/memory/${projectCtrl.text}");
    final res = await http.get(uri);
    setState(() {
      memoryPreview = jsonDecode(res.body);
    });
  }

  Future<void> deployToGithub() async {
    final uri = Uri.parse("http://localhost:8000/agent/deploy-auto");
    final res = await http.post(uri,
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": "supersecret"
        },
        body: jsonEncode({
          "user": userCtrl.text,
          "project": projectCtrl.text,
          "branch": "main",
          "commit_message": messageCtrl.text,
          "repo_url": repoUrlCtrl.text,
          "token": tokenCtrl.text
        }));

    setState(() => output = res.body);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(20),
      child: Column(
        children: [
          TextField(controller: userCtrl, decoration: InputDecoration(labelText: "User")),
          TextField(controller: projectCtrl, decoration: InputDecoration(labelText: "Project")),
          TextField(controller: messageCtrl, decoration: InputDecoration(labelText: "Commit Message")),
          TextField(controller: tokenCtrl, decoration: InputDecoration(labelText: "GitHub Token"), obscureText: true),
          TextField(controller: repoUrlCtrl, decoration: InputDecoration(labelText: "GitHub Repo URL")),
          ElevatedButton(onPressed: fetchMemoryPreview, child: Text("🔍 Preview Memory")),
          SizedBox(height: 10),
          Expanded(
            child: ListView(
              children: memoryPreview.entries.map((entry) => ListTile(
                title: Text(entry.key),
                subtitle: Text(entry.value.toString().substring(0, 100) + "..."),
              )).toList(),
            ),
          ),
          ElevatedButton(onPressed: deployToGithub, child: Text("🚀 Push to GitHub")),
          SizedBox(height: 10),
          SelectableText(output),
        ],
      ),
    );
  }
}
