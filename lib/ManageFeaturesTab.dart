
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ManageFeaturesTab extends StatefulWidget {
  @override
  _ManageFeaturesTabState createState() => _ManageFeaturesTabState();
}

class _ManageFeaturesTabState extends State<ManageFeaturesTab> {
  final projectCtrl = TextEditingController();
  final featureCtrl = TextEditingController();
  final planCtrl = TextEditingController();
  final codeCtrl = TextEditingController();
  final testCtrl = TextEditingController();

  List<String> features = [];
  String selectedFeature = "";
  String response = "";

  Future<void> loadFeatures() async {
    final res = await http.get(Uri.parse("http://localhost:8000/features/${projectCtrl.text}"));
    if (res.statusCode == 200) {
      setState(() {
        features = List<String>.from(jsonDecode(res.body));
        selectedFeature = features.isNotEmpty ? features[0] : "";
      });
    }
  }

  Future<void> deleteFeature() async {
    final res = await http.delete(Uri.parse("http://localhost:8000/features/${projectCtrl.text}/$selectedFeature"));
    setState(() => response = res.body);
    loadFeatures(); // refresh list
  }

  Future<void> modifyFeature() async {
    final uri = Uri.parse("http://localhost:8000/features/${projectCtrl.text}/$selectedFeature");
    final payload = {
      "output": {
        "plan": planCtrl.text,
        "code": codeCtrl.text,
        "test": testCtrl.text
      }
    };
    final res = await http.put(uri,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(payload));
    setState(() => response = res.body);
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: EdgeInsets.all(20),
      children: [
        TextField(controller: projectCtrl, decoration: InputDecoration(labelText: "Project Name")),
        ElevatedButton(onPressed: loadFeatures, child: Text("🔍 Load Features")),
        if (features.isNotEmpty)
          DropdownButton<String>(
            value: selectedFeature,
            onChanged: (val) => setState(() => selectedFeature = val ?? ""),
            items: features.map((f) => DropdownMenuItem(value: f, child: Text(f))).toList(),
          ),
        TextField(controller: planCtrl, decoration: InputDecoration(labelText: "Updated Plan")),
        TextField(controller: codeCtrl, decoration: InputDecoration(labelText: "Updated Code"), maxLines: 5),
        TextField(controller: testCtrl, decoration: InputDecoration(labelText: "Updated Test"), maxLines: 5),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            ElevatedButton(onPressed: modifyFeature, child: Text("♻️ Modify Feature")),
            ElevatedButton(onPressed: deleteFeature, child: Text("🗑 Remove Feature")),
          ],
        ),
        SizedBox(height: 10),
        SelectableText(response),
      ],
    );
  }
}
