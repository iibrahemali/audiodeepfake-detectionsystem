#!/usr/bin/env dart

//import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'dart:convert';

const String backendUrl = 'http://localhost:8000';

void main() async {
  print('🧪 Testing Frontend Integration');
  print('=' * 50);
  
  await testBackendConnection();
  await testHealthEndpoint();
  await testUploadCapabilities();
  
  print('\n' + '=' * 50);
  print('✅ All integration tests completed!');
}

Future<void> testBackendConnection() async {
  print('\n🔍 Testing backend connection...');
  
  try {
    final response = await http.get(
      Uri.parse('$backendUrl/health'),
      headers: {'Content-Type': 'application/json'},
    ).timeout(Duration(seconds: 5));
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      print('✅ Backend is online');
      print('   Status: ${data['status']}');
      print('   Model: ${data['model_status']}');
      print('   Version: ${data['version']}');
    } else {
      print('❌ Backend responded with status: ${response.statusCode}');
    }
  } catch (e) {
    print('❌ Cannot connect to backend: $e');
    print('💡 Make sure backend is running: cd ../backend && python run.py');
  }
}

Future<void> testHealthEndpoint() async {
  print('\n🏥 Testing health endpoint...');
  
  try {
    final response = await http.get(Uri.parse('$backendUrl/health'));
    final data = json.decode(response.body);
    
    // Validate response structure
    final requiredFields = ['status', 'model_status', 'version'];
    bool allFieldsPresent = requiredFields.every((field) => data.containsKey(field));
    
    if (allFieldsPresent) {
      print('✅ Health endpoint structure is correct');
    } else {
      print('❌ Health endpoint missing required fields');
    }
    
  } catch (e) {
    print('❌ Health endpoint test failed: $e');
  }
}

Future<void> testUploadCapabilities() async {
  print('\n📤 Testing upload capabilities...');
  
  // Create a minimal WAV file for testing
  final testWavData = createMinimalWavFile();
  
  try {
    var request = http.MultipartRequest('POST', Uri.parse('$backendUrl/predict/'));
    request.files.add(
      http.MultipartFile.fromBytes(
        'file',
        testWavData,
        filename: 'test.wav',
      ),
    );
    
    final response = await request.send().timeout(Duration(seconds: 30));
    final responseBody = await response.stream.bytesToString();
    
    if (response.statusCode == 200) {
      final data = json.decode(responseBody);
      
      // Validate prediction response structure
      final requiredFields = ['result', 'score', 'confidence', 'threshold', 'model_type'];
      bool allFieldsPresent = requiredFields.every((field) => data.containsKey(field));
      
      if (allFieldsPresent) {
        print('✅ Upload and prediction successful');
        print('   Result: ${data['result']}');
        print('   Score: ${data['score']}');
        print('   Confidence: ${data['confidence']}');
        print('   Model: ${data['model_type']}');
      } else {
        print('❌ Prediction response missing required fields');
      }
    } else {
      print('❌ Upload failed with status: ${response.statusCode}');
      print('   Response: $responseBody');
    }
    
  } catch (e) {
    print('❌ Upload test failed: $e');
    print('💡 Make sure AASIST model is loaded in backend');
  }
}

Uint8List createMinimalWavFile() {
  // Create a minimal 16-bit WAV file (1 second, 16kHz, mono)
  final sampleRate = 16000;
  final duration = 1; // seconds
  final numSamples = sampleRate * duration;
  
  // WAV header (44 bytes)
  final header = <int>[
    // RIFF header
    0x52, 0x49, 0x46, 0x46, // "RIFF"
    0x00, 0x00, 0x00, 0x00, // File size (will be filled later)
    0x57, 0x41, 0x56, 0x45, // "WAVE"
    
    // Format chunk
    0x66, 0x6D, 0x74, 0x20, // "fmt "
    0x10, 0x00, 0x00, 0x00, // Chunk size (16)
    0x01, 0x00,             // Audio format (PCM)
    0x01, 0x00,             // Number of channels (1)
    0x00, 0x3E, 0x00, 0x00, // Sample rate (16000)
    0x00, 0x7D, 0x00, 0x00, // Byte rate (32000)
    0x02, 0x00,             // Block align (2)
    0x10, 0x00,             // Bits per sample (16)
    
    // Data chunk
    0x64, 0x61, 0x74, 0x61, // "data"
    0x00, 0x00, 0x00, 0x00, // Data size (will be filled later)
  ];
  
  // Generate simple sine wave data
  final data = <int>[];
  for (int i = 0; i < numSamples; i++) {
    // Generate a 440Hz sine wave
    final sample = (32767 * 0.1 * Math.sin(2 * Math.pi * 440 * i / sampleRate)).round();
    data.add(sample & 0xFF);        // Low byte
    data.add((sample >> 8) & 0xFF); // High byte
  }
  
  // Update file size in header
  final fileSize = header.length + data.length - 8;
  header[4] = fileSize & 0xFF;
  header[5] = (fileSize >> 8) & 0xFF;
  header[6] = (fileSize >> 16) & 0xFF;
  header[7] = (fileSize >> 24) & 0xFF;
  
  // Update data size in header
  final dataSize = data.length;
  header[40] = dataSize & 0xFF;
  header[41] = (dataSize >> 8) & 0xFF;
  header[42] = (dataSize >> 16) & 0xFF;
  header[43] = (dataSize >> 24) & 0xFF;
  
  return Uint8List.fromList([...header, ...data]);
}

// Simple Math class for sine function
class Math {
  static const double pi = 3.141592653589793;
  static double sin(double x) {
    // Simple sine approximation using Taylor series
    double result = x;
    double term = x;
    for (int i = 1; i < 10; i++) {
      term *= -x * x / ((2 * i) * (2 * i + 1));
      result += term;
    }
    return result;
  }
} 