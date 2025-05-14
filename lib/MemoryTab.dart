
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class MemoryTab extends StatefulWidget {
  @override
  _MemoryTabState createState() => _MemoryTabState();
}

class _MemoryTabState extends State<MemoryTab> {
  final TextEditingController projectCtrl = TextEditingController();
  List<dynamic> entries = [];
  bool loading = false;

  Future<void> fetchMemory() async {
    setState(() => loading = true);
    final uri = Uri.parse("http://localhost:8000/memory/${projectCtrl.text}");
    final res = await http.get(uri);
    setState(() {
      loading = false;
      if (res.statusCode == 200) {
        entries = jsonDecode(res.body)['entries'];
      } else {
        entries = [];
      }
    });
  }

  Widget buildMemoryCard(Map memory) {
    return Card(
      margin: EdgeInsets.symmetric(vertical: 10),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("🧠 ${memory['feature']}", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            if (memory['plan'] != null) Text("📋 Plan:\n${memory['plan']}\n"),
            if (memory['code'] != null) Text("💻 Code:\n${memory['code']}\n"),
            if (memory['test'] != null) Text("🧪 Test:\n${memory['test']}\n"),
            if (memory['notes'] != null) Text("📝 Notes:\n${memory['notes']}"),
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
          Text("🔍 View Project Memory", style: Theme.of(context).textTheme.headlineSmall),
          TextField(
            controller: projectCtrl,
            decoration: InputDecoration(labelText: "Enter project name"),
          ),
          SizedBox(height: 10),
          ElevatedButton(onPressed: fetchMemory, child: Text("Fetch Memory")),
          SizedBox(height: 20),
          if (loading) Center(child: CircularProgressIndicator()),
          ...entries.map((e) => buildMemoryCard(e)).toList(),
        ],
      ),
    );
  }
}
