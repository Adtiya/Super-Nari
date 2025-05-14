
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class MemoryTimelineTab extends StatefulWidget {
  @override
  _MemoryTimelineTabState createState() => _MemoryTimelineTabState();
}

class _MemoryTimelineTabState extends State<MemoryTimelineTab> {
  late Future<List<dynamic>> memoryData;
  final TextEditingController _annotationController = TextEditingController();

  @override
  void initState() {
    super.initState();
    memoryData = fetchMemoryData();
  }

  Future<List<dynamic>> fetchMemoryData() async {
    final response = await http.get(
      Uri.parse('http://localhost:8000/memory/view?project=WeatherBot'),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['features'];
    } else {
      throw Exception('Failed to load memory data');
    }
  }

  Future<void> annotateMemory(String featureName, String note) async {
    await http.post(
      Uri.parse('http://localhost:8000/memory/annotate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({"feature_name": featureName, "note": note}),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Memory Timeline")),
      body: FutureBuilder<List<dynamic>>(
        future: memoryData,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: \${snapshot.error}"));
          }

          final features = snapshot.data!;
          return ListView.builder(
            itemCount: features.length,
            itemBuilder: (context, index) {
              final feature = features[index];
              return Card(
                margin: EdgeInsets.all(12),
                child: ListTile(
                  title: Text(feature["feature_name"]),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text("Created: \${feature['created_at']}"),
                      Text("Status: \${feature['status']}"),
                      Text("Prompt: \${feature['prompt']}"),
                    ],
                  ),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: Icon(Icons.code),
                        onPressed: () {
                          showDialog(
                            context: context,
                            builder: (_) => Material(
                              child: AlertDialog(
                                title: Text("Code for \${feature['feature_name']}"),
                                content: SingleChildScrollView(
                                  child: Text(feature["code"]),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                      IconButton(
                        icon: Icon(Icons.edit),
                        onPressed: () {
                          _annotationController.clear();
                          showDialog(
                            context: context,
                            builder: (_) => Material(
                              child: AlertDialog(
                                title: Text("Annotate Memory"),
                                content: TextField(
                                  controller: _annotationController,
                                  maxLines: 4,
                                  decoration: InputDecoration(
                                    hintText: "Enter annotation...",
                                  ),
                                ),
                                actions: [
                                  TextButton(
                                    child: Text("Save"),
                                    onPressed: () async {
                                      await annotateMemory(
                                          feature["feature_name"],
                                          _annotationController.text);
                                      Navigator.pop(context);
                                    },
                                  )
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
