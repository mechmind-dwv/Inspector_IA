import React, { useState, useEffect } from 'react';
import { Camera, AlertTriangle, TrendingUp, Users, Activity, ChevronRight, Search, Filter, Download, Eye, Network, Clock, DollarSign, Globe, Shield } from 'lucide-react';

// Main Dashboard Application
const InspectorIADashboard = () => {
  const [activeView, setActiveView] = useState('overview');
  const [selectedCase, setSelectedCase] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [timeRange, setTimeRange] = useState('30d');

  // Sample data for demonstration
  const alertData = [
    {
      id: 1,
      politicianName: "María González",
      position: "Senadora",
      iraScore: 78,
      riskLevel: "Supernova Alert",
      primaryPattern: "CRYPTO_HIDING",
      detectionDate: "2024-12-10",
      flagCount: 5,
      confidence: 0.87,
      hiddenAmount: 450000,
      techniques: ["Mixer Cascade", "Privacy Coins", "Cross-Chain"],
      status: "under_investigation"
    },
    {
      id: 2,
      politicianName: "Carlos Mendoza",
      position: "Diputado",
      iraScore: 64,
      riskLevel: "Stellar Anomaly",
      primaryPattern: "OFFSHORE_LAUNDERING",
      detectionDate: "2024-12-08",
      flagCount: 3,
      confidence: 0.72,
      hiddenAmount: 850000,
      techniques: ["Shell Companies", "Nominee Shareholders"],
      status: "initial_review"
    },
    {
      id: 3,
      politicianName: "Ana Rodríguez",
      position: "Alcaldesa",
      iraScore: 56,
      riskLevel: "Stellar Anomaly",
      primaryPattern: "GHOST_COMPANY",
      detectionDate: "2024-12-12",
      flagCount: 4,
      confidence: 0.81,
      hiddenAmount: 320000,
      techniques: ["Low Activity Entities", "High Contracts"],
      status: "new"
    }
  ];

  const systemStats = {
    totalPoliticians: 12847,
    activeAlerts: 23,
    patternsDetected: 156,
    investigationsActive: 8,
    averageIRA: 24.3,
    systemHealth: 98
  };

  // Risk level color mapping
  const getRiskColor = (level) => {
    const colors = {
      "Black Hole Critical": "bg-black text-white",
      "Supernova Alert": "bg-red-600 text-white",
      "Stellar Anomaly": "bg-orange-500 text-white",
      "Nebular Suspicion": "bg-yellow-500 text-gray-900",
      "Cosmic Background": "bg-green-600 text-white"
    };
    return colors[level] || "bg-gray-500 text-white";
  };

  // IRA Score visualization component
  const IRAScoreGauge = ({ score }) => {
    const getScoreColor = () => {
      if (score >= 86) return '#000000';
      if (score >= 71) return '#dc2626';
      if (score >= 51) return '#f97316';
      if (score >= 21) return '#eab308';
      return '#16a34a';
    };

    const circumference = 2 * Math.PI * 45;
    const progress = (score / 100) * circumference;

    return (
      <div className="relative w-32 h-32">
        <svg className="transform -rotate-90 w-32 h-32">
          <circle
            cx="64"
            cy="64"
            r="45"
            stroke="#e5e7eb"
            strokeWidth="8"
            fill="none"
          />
          <circle
            cx="64"
            cy="64"
            r="45"
            stroke={getScoreColor()}
            strokeWidth="8"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={circumference - progress}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-2xl font-bold" style={{ color: getScoreColor() }}>
              {score}
            </div>
            <div className="text-xs text-gray-500">IRA</div>
          </div>
        </div>
      </div>
    );
  };

  // Header Component
  const Header = () => (
    <header className="bg-gradient-to-r from-indigo-900 to-purple-900 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-white p-2 rounded-lg">
              <Shield className="w-8 h-8 text-indigo-900" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Inspector IA</h1>
              <p className="text-indigo-200 text-sm">Forensic Intelligence for Public Accountability</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <div className="text-sm text-indigo-200">System Status</div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm font-semibold">Operational {systemStats.systemHealth}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );

  // Navigation Component
  const Navigation = () => (
    <nav className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex space-x-8">
          {[
            { id: 'overview', label: 'Overview', icon: Activity },
            { id: 'alerts', label: 'Active Alerts', icon: AlertTriangle },
            { id: 'network', label: 'Network Analysis', icon: Network },
            { id: 'patterns', label: 'Pattern Detection', icon: TrendingUp },
            { id: 'investigations', label: 'Investigations', icon: Eye }
          ].map(item => (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`flex items-center space-x-2 px-3 py-4 border-b-2 font-medium text-sm transition-colors ${
                activeView === item.id
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <item.icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  );

  // Statistics Cards Component
  const StatCard = ({ title, value, icon: Icon, trend, color }) => (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4" style={{ borderColor: color }}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {trend && (
            <p className={`text-xs mt-1 ${trend > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% from last month
            </p>
          )}
        </div>
        <div className="p-3 rounded-full" style={{ backgroundColor: color + '20' }}>
          <Icon className="w-6 h-6" style={{ color }} />
        </div>
      </div>
    </div>
  );

  // Overview Dashboard View
  const OverviewView = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Politicians Monitored"
          value={systemStats.totalPoliticians.toLocaleString()}
          icon={Users}
          color="#4f46e5"
        />
        <StatCard
          title="Active Alerts"
          value={systemStats.activeAlerts}
          icon={AlertTriangle}
          trend={12}
          color="#dc2626"
        />
        <StatCard
          title="Patterns Detected"
          value={systemStats.patternsDetected}
          icon={TrendingUp}
          trend={8}
          color="#f97316"
        />
        <StatCard
          title="Active Investigations"
          value={systemStats.investigationsActive}
          icon={Eye}
          color="#16a34a"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h3>
          <div className="space-y-3">
            {[
              { level: 'Black Hole Critical (86-100)', count: 2, color: '#000000' },
              { level: 'Supernova Alert (71-85)', count: 5, color: '#dc2626' },
              { level: 'Stellar Anomaly (51-70)', count: 16, color: '#f97316' },
              { level: 'Nebular Suspicion (21-50)', count: 47, color: '#eab308' },
              { level: 'Cosmic Background (0-20)', count: 12777, color: '#16a34a' }
            ].map(item => {
              const percentage = (item.count / systemStats.totalPoliticians) * 100;
              return (
                <div key={item.level}>
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className="text-gray-700">{item.level}</span>
                    <span className="font-semibold">{item.count}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-500"
                      style={{ width: `${percentage}%`, backgroundColor: item.color }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Pattern Breakdown</h3>
          <div className="space-y-4">
            {[
              { name: 'CRYPTO_HIDING', count: 42, percentage: 27 },
              { name: 'OFFSHORE_LAUNDERING', count: 38, percentage: 24 },
              { name: 'GHOST_COMPANY', count: 31, percentage: 20 },
              { name: 'INSIDER_TRADING', count: 28, percentage: 18 },
              { name: 'TRAVEL_COINCIDENCE', count: 17, percentage: 11 }
            ].map(pattern => (
              <div key={pattern.name} className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">{pattern.name}</span>
                    <span className="text-sm text-gray-600">{pattern.count}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-1.5">
                    <div
                      className="bg-indigo-600 h-1.5 rounded-full transition-all"
                      style={{ width: `${pattern.percentage}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  // Alert Card Component
  const AlertCard = ({ alert, onSelect }) => (
    <div
      onClick={() => onSelect(alert)}
      className="bg-white rounded-lg shadow-md p-6 border-l-4 hover:shadow-lg transition-shadow cursor-pointer"
      style={{
        borderColor: alert.iraScore >= 71 ? '#dc2626' : alert.iraScore >= 51 ? '#f97316' : '#eab308'
      }}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-3">
            <h3 className="text-lg font-semibold text-gray-900">{alert.politicianName}</h3>
            <span className={`px-2 py-1 rounded text-xs font-semibold ${getRiskColor(alert.riskLevel)}`}>
              {alert.riskLevel}
            </span>
          </div>
          <p className="text-sm text-gray-600 mb-4">{alert.position}</p>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="flex items-center space-x-2">
              <DollarSign className="w-4 h-4 text-gray-400" />
              <div>
                <div className="text-xs text-gray-500">Hidden Amount</div>
                <div className="text-sm font-semibold">${(alert.hiddenAmount / 1000).toFixed(0)}K</div>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-gray-400" />
              <div>
                <div className="text-xs text-gray-500">Detection Date</div>
                <div className="text-sm font-semibold">{alert.detectionDate}</div>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 mb-3">
            {alert.techniques.map((tech, idx) => (
              <span key={idx} className="px-2 py-1 bg-indigo-100 text-indigo-700 text-xs rounded-full">
                {tech}
              </span>
            ))}
          </div>

          <div className="flex items-center justify-between pt-3 border-t border-gray-200">
            <div className="flex items-center space-x-4">
              <div className="text-xs text-gray-500">
                Primary Pattern: <span className="font-semibold text-gray-700">{alert.primaryPattern}</span>
              </div>
              <div className="text-xs text-gray-500">
                Confidence: <span className="font-semibold text-gray-700">{(alert.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
            <ChevronRight className="w-5 h-5 text-gray-400" />
          </div>
        </div>
        <div className="ml-4">
          <IRAScoreGauge score={alert.iraScore} />
        </div>
      </div>
    </div>
  );

  // Alerts View
  const AlertsView = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 flex-1">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search by politician name, pattern, or ID..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              <Filter className="w-4 h-4" />
              <span>Filter</span>
            </button>
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {alertData.map(alert => (
          <AlertCard key={alert.id} alert={alert} onSelect={setSelectedCase} />
        ))}
      </div>
    </div>
  );

  // Case Detail Modal
  const CaseDetailModal = ({ caseData, onClose }) => {
    if (!caseData) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{caseData.politicianName}</h2>
              <p className="text-gray-600">{caseData.position}</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
            >
              ×
            </button>
          </div>

          <div className="p-6 space-y-6">
            <div className="grid grid-cols-2 gap-6">
              <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Risk Assessment</h3>
                  <IRAScoreGauge score={caseData.iraScore} />
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Risk Level:</span>
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${getRiskColor(caseData.riskLevel)}`}>
                      {caseData.riskLevel}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Confidence:</span>
                    <span className="font-semibold">{(caseData.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Detection Flags:</span>
                    <span className="font-semibold">{caseData.flagCount}</span>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Financial Impact</h3>
                <div className="space-y-3">
                  <div>
                    <div className="text-sm text-gray-600">Estimated Hidden Amount</div>
                    <div className="text-3xl font-bold text-gray-900">
                      ${(caseData.hiddenAmount / 1000).toFixed(0)}K
                    </div>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Primary Pattern:</span>
                    <span className="font-semibold">{caseData.primaryPattern}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Detection Date:</span>
                    <span className="font-semibold">{caseData.detectionDate}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Detection Techniques</h3>
              <div className="flex flex-wrap gap-3">
                {caseData.techniques.map((tech, idx) => (
                  <div key={idx} className="flex items-center space-x-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg">
                    <AlertTriangle className="w-4 h-4" />
                    <span className="font-medium">{tech}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">XAI Explanation</h3>
                  <p className="text-gray-700 leading-relaxed">
                    This case exhibits a sophisticated CRYPTO_HIDING pattern with an IRA score of {caseData.iraScore}. 
                    The system detected {caseData.flagCount} distinct anomaly flags including the use of mixer services, 
                    privacy coin conversions, and cross-chain bridge transactions. The estimated hidden amount of 
                    ${(caseData.hiddenAmount / 1000).toFixed(0)}K significantly exceeds declared income patterns. 
                    The detection confidence of {(caseData.confidence * 100).toFixed(0)}% is based on multi-dimensional 
                    analysis including network topology, temporal patterns, and transaction characteristics. 
                    Human verification is required before any investigative action.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex space-x-4">
              <button className="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold">
                Start Investigation
              </button>
              <button className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-semibold">
                Export Report
              </button>
              <button className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-semibold">
                Request More Data
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Main Render
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Navigation />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeView === 'overview' && <OverviewView />}
        {activeView === 'alerts' && <AlertsView />}
        {activeView === 'network' && (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <Network className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Network Analysis</h3>
            <p className="text-gray-600">Network visualization and graph analysis tools coming soon.</p>
          </div>
        )}
        {activeView === 'patterns' && (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <TrendingUp className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Pattern Detection</h3>
            <p className="text-gray-600">Advanced pattern detection and analysis tools coming soon.</p>
          </div>
        )}
        {activeView === 'investigations' && (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <Eye className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Active Investigations</h3>
            <p className="text-gray-600">Investigation management and collaboration tools coming soon.</p>
          </div>
        )}
      </main>

      <CaseDetailModal caseData={selectedCase} onClose={() => setSelectedCase(null)} />
    </div>
  );
};

export default InspectorIADashboard;
