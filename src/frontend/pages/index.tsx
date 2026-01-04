import InspectorIADashboard from '../components/InspectorIADashboard';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            Inspector IA - Forensic Dashboard
          </h1>
          <p className="mt-2 text-gray-600">
            Sistema de detección de anomalías para periodismo investigativo
          </p>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 px-4">
        <InspectorIADashboard />
      </main>
    </div>
  );
}
