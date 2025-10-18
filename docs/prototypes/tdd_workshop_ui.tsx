import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, Play, RotateCcw, Eye, Code, TestTube, Zap, AlertCircle, CheckCircle2, XCircle, Clock } from 'lucide-react';

export default function TDDWorkshopUI() {
  const [phase, setPhase] = useState('red');
  const [code, setCode] = useState('def add(a, b):\n    pass');
  const [mockSet, setMockSet] = useState('valid');
  const [testsRun, setTestsRun] = useState(false);
  const [expandedTest, setExpandedTest] = useState(0);
  const [showRefactorGuide, setShowRefactorGuide] = useState(false);

  const tests = [
    {
      id: 1,
      name: 'test_add_positive_numbers',
      status: 'fail',
      mocks: { inputs: [2, 3], expected: 5 },
      actual: null,
      assertion: 'assertEqual(add(2, 3), 5)',
      error: 'Expected 5, got None'
    },
    {
      id: 2,
      name: 'test_add_negative_numbers',
      status: 'fail',
      mocks: { inputs: [-1, -2], expected: -3 },
      actual: null,
      assertion: 'assertEqual(add(-1, -2), -3)',
      error: 'Expected -3, got None'
    },
    {
      id: 3,
      name: 'test_add_zero',
      status: 'fail',
      mocks: { inputs: [5, 0], expected: 5 },
      actual: null,
      assertion: 'assertEqual(add(5, 0), 5)',
      error: 'Expected 5, got None'
    },
    {
      id: 4,
      name: 'test_add_floats',
      status: 'fail',
      mocks: { inputs: [2.5, 3.7], expected: 6.2 },
      actual: null,
      assertion: 'assertAlmostEqual(add(2.5, 3.7), 6.2)',
      error: 'Expected 6.2, got None'
    },
    {
      id: 5,
      name: 'test_add_large_numbers',
      status: 'fail',
      mocks: { inputs: [999999, 1], expected: 1000000 },
      actual: null,
      assertion: 'assertEqual(add(999999, 1), 1000000)',
      error: 'Expected 1000000, got None'
    }
  ];

  const mockSets = {
    valid: {
      name: 'Valid Inputs',
      description: 'Basic positive numbers',
      dataPoints: 3
    },
    edge: {
      name: 'Edge Cases',
      description: 'Zero, negatives, floats',
      dataPoints: 5
    },
    stress: {
      name: 'Stress Test',
      description: 'Large numbers, performance',
      dataPoints: 2
    }
  };

  const codeMetrics = {
    complexity: 1,
    coverage: 0,
    lines: 2,
    duplicates: 0
  };

  const passedTests = 0;
  const totalTests = 5;

  return (
    <div className="h-screen bg-slate-950 text-slate-50 flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 border-b border-slate-700 px-6 py-4">
        <div className="flex justify-between items-center mb-3">
          <div>
            <h1 className="text-2xl font-bold">Build an Add Function</h1>
            <p className="text-slate-400 text-sm">Module: Fundamentals • Workshop 1 of 4</p>
          </div>
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition">← Back</button>
            <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition">Help</button>
          </div>
        </div>

        {/* Phase Indicator */}
        <div className="flex gap-3">
          {[
            { key: 'red', label: '🔴 RED: See Failing Tests', color: 'bg-red-900' },
            { key: 'green', label: '🟢 GREEN: Make Tests Pass', color: 'bg-green-900' },
            { key: 'refactor', label: '🔵 REFACTOR: Improve Code', color: 'bg-blue-900' }
          ].map(p => (
            <button
              key={p.key}
              onClick={() => setPhase(p.key)}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                phase === p.key
                  ? `${p.color} ring-2 ring-offset-2 ring-offset-slate-900`
                  : 'bg-slate-700 hover:bg-slate-600'
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex gap-4 p-4 overflow-hidden">
        
        {/* LEFT PANEL: Tests */}
        <div className="w-80 bg-slate-900 rounded-lg border border-slate-700 flex flex-col overflow-hidden">
          <div className="bg-slate-800 px-4 py-3 border-b border-slate-700">
            <h2 className="font-bold flex items-center gap-2">
              <TestTube size={18} className="text-red-400" />
              Test Suite ({passedTests}/{totalTests})
            </h2>
          </div>

          {/* Test Progress Bar */}
          <div className="px-4 py-3 bg-slate-800 border-b border-slate-700">
            <div className="flex justify-between text-xs text-slate-400 mb-2">
              <span>Progress</span>
              <span>{Math.round((passedTests / totalTests) * 100)}%</span>
            </div>
            <div className="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-red-500 to-orange-500 h-full transition-all"
                style={{ width: `${(passedTests / totalTests) * 100}%` }}
              />
            </div>
          </div>

          {/* Tests List */}
          <div className="flex-1 overflow-y-auto space-y-2 p-3">
            {tests.map((test, idx) => (
              <button
                key={test.id}
                onClick={() => setExpandedTest(expandedTest === idx ? -1 : idx)}
                className={`w-full text-left p-3 rounded-lg border transition ${
                  test.status === 'fail'
                    ? 'bg-red-950 border-red-700 hover:bg-red-900'
                    : 'bg-green-950 border-green-700 hover:bg-green-900'
                }`}
              >
                <div className="flex items-start gap-2">
                  {test.status === 'fail' ? (
                    <XCircle size={18} className="text-red-400 flex-shrink-0 mt-0.5" />
                  ) : (
                    <CheckCircle2 size={18} className="text-green-400 flex-shrink-0 mt-0.5" />
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="font-mono text-sm truncate">{test.name}</p>
                    <p className="text-xs text-slate-400 mt-1">
                      Input: {JSON.stringify(test.mocks.inputs)} → {test.mocks.expected}
                    </p>
                  </div>
                </div>

                {/* Expanded Test Details */}
                {expandedTest === idx && (
                  <div className="mt-3 pt-3 border-t border-slate-700 text-xs space-y-2">
                    <div className="bg-slate-950 rounded p-2 font-mono">
                      <p className="text-slate-400">Assertion:</p>
                      <p className="text-blue-300">{test.assertion}</p>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <div className="bg-slate-950 rounded p-2">
                        <p className="text-slate-400">Expected</p>
                        <p className="text-green-300 font-mono">{test.mocks.expected}</p>
                      </div>
                      <div className="bg-slate-950 rounded p-2">
                        <p className="text-slate-400">Got</p>
                        <p className="text-red-300 font-mono">{test.actual || 'None'}</p>
                      </div>
                    </div>
                    <div className="bg-red-950 border border-red-700 rounded p-2">
                      <p className="text-red-200">{test.error}</p>
                    </div>
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* CENTER PANEL: Code Editor */}
        <div className="flex-1 bg-slate-900 rounded-lg border border-slate-700 flex flex-col overflow-hidden">
          <div className="bg-slate-800 px-4 py-3 border-b border-slate-700 flex justify-between items-center">
            <h2 className="font-bold flex items-center gap-2">
              <Code size={18} className="text-blue-400" />
              Code Editor
            </h2>
            <div className="text-xs text-slate-400">
              {phase === 'red' && '🔴 Analyze tests, then write code'}
              {phase === 'green' && '🟢 Make all tests pass'}
              {phase === 'refactor' && '🔵 Improve while keeping tests green'}
            </div>
          </div>

          {/* Editor */}
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="flex-1 bg-slate-950 text-slate-100 font-mono p-4 resize-none focus:outline-none border-0"
            spellCheck="false"
          />

          {/* Editor Footer */}
          <div className="bg-slate-800 border-t border-slate-700 px-4 py-3 flex justify-between items-center">
            <div className="text-xs text-slate-400">
              Lines: {code.split('\n').length} | Column: {code.split('\n')[code.split('\n').length - 1].length}
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setCode('def add(a, b):\n    pass')}
                className="px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded text-sm flex items-center gap-2 transition"
              >
                <RotateCcw size={14} /> Reset
              </button>
              <button
                onClick={() => setTestsRun(true)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded text-sm font-semibold flex items-center gap-2 transition"
              >
                <Play size={14} /> Run Tests
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT PANEL: Mock Data + Metrics */}
        <div className="w-80 flex flex-col gap-4 overflow-hidden">
          
          {/* Mock Data Selector */}
          <div className="bg-slate-900 rounded-lg border border-slate-700 flex flex-col overflow-hidden">
            <div className="bg-slate-800 px-4 py-3 border-b border-slate-700">
              <h2 className="font-bold flex items-center gap-2">
                <Zap size={18} className="text-yellow-400" />
                Mock Data Sets
              </h2>
            </div>

            <div className="p-3 space-y-2 flex-1">
              {Object.entries(mockSets).map(([key, set]) => (
                <button
                  key={key}
                  onClick={() => setMockSet(key)}
                  className={`w-full text-left p-3 rounded-lg border transition ${
                    mockSet === key
                      ? 'bg-yellow-950 border-yellow-600 ring-2 ring-yellow-500'
                      : 'bg-slate-800 border-slate-700 hover:border-slate-600'
                  }`}
                >
                  <div className="font-semibold text-sm">{set.name}</div>
                  <p className="text-xs text-slate-400 mt-1">{set.description}</p>
                  <p className="text-xs text-slate-500 mt-1">{set.dataPoints} data points</p>
                </button>
              ))}
            </div>

            {/* Mock Data Preview */}
            <div className="bg-slate-800 border-t border-slate-700 px-4 py-3">
              <p className="text-xs font-semibold text-slate-400 mb-2">Current Mock Data:</p>
              <div className="bg-slate-950 rounded p-2 font-mono text-xs text-slate-300 max-h-20 overflow-y-auto">
                {mockSet === 'valid' && 'inputs: [2, 3, 5, 0]'}
                {mockSet === 'edge' && 'inputs: [0, -5, 2.5, -0.1]'}
                {mockSet === 'stress' && 'inputs: [999999, 1e6]'}
              </div>
            </div>
          </div>

          {/* Code Metrics & Refactor Guide */}
          {phase === 'refactor' && (
            <div className="bg-slate-900 rounded-lg border border-slate-700 flex flex-col overflow-hidden">
              <div className="bg-slate-800 px-4 py-3 border-b border-slate-700">
                <h2 className="font-bold flex items-center gap-2">
                  📊 Code Metrics
                </h2>
              </div>

              <div className="p-4 space-y-3">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Cyclomatic Complexity</span>
                    <span className="text-green-400 font-semibold">{codeMetrics.complexity}</span>
                  </div>
                  <div className="bg-slate-800 rounded h-2 overflow-hidden">
                    <div className="bg-green-500 h-full w-1/4" />
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Test Coverage</span>
                    <span className="text-orange-400 font-semibold">{codeMetrics.coverage}%</span>
                  </div>
                  <div className="bg-slate-800 rounded h-2 overflow-hidden">
                    <div className="bg-orange-500 h-full w-0" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-slate-800 rounded p-2">
                    <p className="text-slate-400">Lines</p>
                    <p className="text-lg font-bold">{codeMetrics.lines}</p>
                  </div>
                  <div className="bg-slate-800 rounded p-2">
                    <p className="text-slate-400">Duplicates</p>
                    <p className="text-lg font-bold">{codeMetrics.duplicates}</p>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800 border-t border-slate-700 px-4 py-3">
                <button
                  onClick={() => setShowRefactorGuide(!showRefactorGuide)}
                  className="w-full text-sm font-semibold text-left flex items-center gap-2 hover:text-blue-300 transition"
                >
                  {showRefactorGuide ? '▼' : '▶'} View Mentor Refactoring
                </button>
                {showRefactorGuide && (
                  <div className="mt-3 text-xs space-y-2 bg-slate-950 rounded p-2">
                    <p className="text-slate-400">💡 Your code works! Consider:</p>
                    <ul className="text-slate-300 space-y-1 list-disc list-inside">
                      <li>Add type hints for clarity</li>
                      <li>Consider edge case handling</li>
                      <li>Add docstring documentation</li>
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Hints Panel */}
          <div className="bg-slate-900 rounded-lg border border-slate-700 overflow-hidden">
            <div className="bg-slate-800 px-4 py-3 border-b border-slate-700">
              <h2 className="font-bold flex items-center gap-2">
                💡 Hints
              </h2>
            </div>
            <div className="p-4 space-y-2">
              {phase === 'red' && (
                <p className="text-sm text-slate-300">
                  📖 <strong>Task:</strong> Implement a function that adds two numbers and returns the result.
                </p>
              )}
              {phase === 'green' && (
                <>
                  <p className="text-sm text-slate-300">
                    💡 <strong>Hint 1:</strong> The function should accept two parameters.
                  </p>
                  <button className="text-xs text-blue-400 hover:text-blue-300 mt-2">
                    Show Hint 2
                  </button>
                </>
              )}
              {phase === 'refactor' && (
                <p className="text-sm text-slate-300">
                  ✨ <strong>Hint:</strong> Refactoring doesn't change what the code does—it improves how it's written.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-slate-900 border-t border-slate-700 px-6 py-3 flex justify-between items-center">
        <div className="text-sm text-slate-400">
          {phase === 'red' && '📖 Understanding the requirements is the first step'}
          {phase === 'green' && testsRun && `⚡ ${passedTests}/${totalTests} tests passing`}
          {phase === 'refactor' && '✨ Keep all tests green while improving quality'}
        </div>
        <div className="flex gap-2">
          <button className="px-3 py-2 text-sm bg-slate-700 hover:bg-slate-600 rounded transition">
            <ChevronLeft size={16} />
          </button>
          <button className="px-3 py-2 text-sm bg-slate-700 hover:bg-slate-600 rounded transition">
            <ChevronRight size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}