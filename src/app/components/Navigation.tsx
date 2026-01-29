import logoImage from '/images/bima bot logo.jpg.jpeg';

interface NavigationProps {
  currentPage: string;
  onNavigate: (page: 'home' | 'audit-bill' | 'how-it-works' | 'about') => void;
}

export default function Navigation({ currentPage, onNavigate }: NavigationProps) {
  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'how-it-works', label: 'How It Works' },
    { id: 'about', label: 'About' }
  ];

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <button
            onClick={() => onNavigate('home')}
            className="flex items-center gap-2 hover:opacity-80 transition-opacity"
          >
            <img src={logoImage} alt="Bima Bot" className="h-8 w-8" />
            <span className="text-xl text-slate-700">Bima Bot</span>
          </button>

          {/* Navigation Links */}
          <div className="flex items-center gap-8">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  if (item.id === 'home' || item.id === 'how-it-works' || item.id === 'about') {
                    onNavigate(item.id as 'home' | 'how-it-works' | 'about');
                  }
                }}
                className={`text-sm transition-colors ${currentPage === item.id
                    ? 'text-[#1E3A8A]'
                    : 'text-gray-600 hover:text-[#1E3A8A]'
                  }`}
              >
                {item.label}
              </button>
            ))}

            {/* CTA Button */}
            <button
              onClick={() => onNavigate('audit-bill')}
              className="bg-[#10B981] hover:bg-[#059669] text-white px-6 py-2 rounded-lg text-sm transition-colors"
            >
              Audit My Hospital Bill
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}