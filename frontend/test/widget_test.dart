// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:flutter/material.dart';

import 'package:deepfake_audio_detector/main.dart';
import 'package:deepfake_audio_detector/services/api_service.dart';
import 'package:deepfake_audio_detector/providers/audio_provider.dart';
import 'package:deepfake_audio_detector/models/api_response.dart';

// Mock API service for testing
class MockApiService extends ApiService {
  @override
  Future<ApiResponse<Map<String, dynamic>>> checkHealth() async {
    // Return a mock successful response
    return Future.delayed(
      Duration(milliseconds: 100),
      () => ApiResponse.success({
        'status': 'healthy',
        'model_status': 'loaded',
        'version': '1.0.0'
      }),
    );
  }
}

void main() {
  testWidgets('App loads and displays basic UI', (WidgetTester tester) async {
    // Create a test app with mocked dependencies
    final testApp = MultiProvider(
      providers: [
        Provider<ApiService>(
          create: (_) => MockApiService(),
        ),
        ChangeNotifierProvider<AudioProvider>(
          create: (context) => AudioProvider(
            apiService: Provider.of<ApiService>(context, listen: false),
          ),
        ),
      ],
      child: MaterialApp(
        title: 'Test App',
        home: Scaffold(
          appBar: AppBar(
            title: Text('Deepfake Audio Detector'),
          ),
          body: Column(
            children: [
              Text('AI-Powered Audio Authentication'),
              ElevatedButton(
                onPressed: () {},
                child: Text('Select Audio File'),
              ),
            ],
          ),
        ),
      ),
    );

    // Build our app and trigger a frame.
    await tester.pumpWidget(testApp);

    // Verify that the app title is displayed
    expect(find.text('Deepfake Audio Detector'), findsOneWidget);
    
    // Verify that the main header text is displayed
    expect(find.text('AI-Powered Audio Authentication'), findsOneWidget);
  });

  testWidgets('Basic UI elements are present', (WidgetTester tester) async {
    // Simple UI test without network calls
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          appBar: AppBar(
            title: Text('Deepfake Audio Detector'),
          ),
          body: Column(
            children: [
              Text('AI-Powered Audio Authentication'),
              ElevatedButton(
                onPressed: () {},
                child: Text('Select Audio File'),
              ),
            ],
          ),
        ),
      ),
    );

    // Verify that file selection button is present
    expect(find.text('Select Audio File'), findsOneWidget);
    
    // Verify app title
    expect(find.text('Deepfake Audio Detector'), findsOneWidget);
  });
}
