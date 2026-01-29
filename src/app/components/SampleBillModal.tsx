import { X } from 'lucide-react';

interface SampleBillModalProps {
  onClose: () => void;
  onRunSampleAudit: () => void;
}

export default function SampleBillModal({ onClose, onRunSampleAudit }: SampleBillModalProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl text-gray-900">Sample Bill & Audit</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
          {/* Left Column - Hospital Bill */}
          <div>
            <h3 className="text-lg mb-4 text-gray-900">Hospital Bill (Sample)</h3>
            <div className="bg-white border-2 border-gray-200 rounded-lg p-6 text-sm">
              <div className="text-center mb-6 pb-4 border-b border-gray-200">
                <h4 className="text-lg text-gray-900 mb-1">Fortis Hospital</h4>
                <p className="text-gray-600">Mumbai, Maharashtra</p>
                <p className="text-gray-600">Bill No: FH/2026/00432</p>
              </div>

              <div className="mb-6">
                <p className="text-gray-700 mb-1"><span className="font-medium">Patient:</span> Rajesh Kumar</p>
                <p className="text-gray-700 mb-1"><span className="font-medium">Admission:</span> 15-Jan-2026</p>
                <p className="text-gray-700 mb-1"><span className="font-medium">Discharge:</span> 18-Jan-2026</p>
                <p className="text-gray-700"><span className="font-medium">Procedure:</span> Appendectomy</p>
              </div>

              <table className="w-full mb-6">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-2 text-gray-700">Description</th>
                    <th className="text-right py-2 text-gray-700">Amount</th>
                  </tr>
                </thead>
                <tbody className="text-gray-700">
                  <tr className="border-b border-gray-100">
                    <td className="py-2">Room Rent (3 days)</td>
                    <td className="text-right">₹24,000</td>
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-2">Surgery Charges</td>
                    <td className="text-right">₹45,000</td>
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-2">Anaesthesia</td>
                    <td className="text-right">₹12,000</td>
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-2">Doctor Consultation</td>
                    <td className="text-right">₹8,000</td>
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-2">Medicines</td>
                    <td className="text-right">₹15,000</td>
                  </tr>
                  <tr className="border-b border-gray-100 bg-amber-50">
                    <td className="py-2">Consumables</td>
                    <td className="text-right">₹8,500</td>
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-2">Lab Tests</td>
                    <td className="text-right">₹6,500</td>
                  </tr>
                  <tr className="border-b border-gray-100 bg-amber-50">
                    <td className="py-2">Service Charges</td>
                    <td className="text-right">₹4,000</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr className="border-t-2 border-gray-300">
                    <td className="py-3 text-gray-900">Total Bill Amount</td>
                    <td className="text-right text-gray-900">₹1,23,000</td>
                  </tr>
                  <tr className="bg-red-50">
                    <td className="py-2 text-gray-900">Deductions Applied</td>
                    <td className="text-right text-red-700">-₹12,500</td>
                  </tr>
                  <tr className="border-t border-gray-200">
                    <td className="py-3 text-gray-900">Insurance Payout</td>
                    <td className="text-right text-gray-900">₹1,10,500</td>
                  </tr>
                  <tr className="bg-gray-100">
                    <td className="py-3 text-lg text-gray-900">Patient Payable</td>
                    <td className="text-right text-lg text-gray-900">₹12,500</td>
                  </tr>
                </tfoot>
              </table>

              <p className="text-xs text-gray-500 italic">
                * Highlighted items flagged during audit
              </p>
            </div>
          </div>

          {/* Right Column - Insurance Policy Extract */}
          <div>
            <h3 className="text-lg mb-4 text-gray-900">Insurance Policy Extract (Sample)</h3>
            <div className="bg-white border-2 border-gray-200 rounded-lg p-6 text-sm">
              <div className="mb-6 pb-4 border-b border-gray-200">
                <h4 className="text-lg text-gray-900 mb-1">Health Insurance Policy</h4>
                <p className="text-gray-600">Policy No: HDFC/ERG/2025/12345</p>
                <p className="text-gray-600">Sum Insured: ₹5,00,000</p>
              </div>

              <div className="space-y-4">
                <div>
                  <h5 className="text-gray-900 mb-2">Coverage Details</h5>
                  <p className="text-gray-700 leading-relaxed">
                    This policy covers hospitalization expenses including room rent, 
                    surgery, doctor fees, medicines, and diagnostic tests.
                  </p>
                </div>

                <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                  <h5 className="text-gray-900 mb-2">Clause 4.2: Room Rent</h5>
                  <p className="text-gray-700 leading-relaxed">
                    Room rent is covered up to ₹8,000 per day for single private AC room.
                  </p>
                </div>

                <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
                  <h5 className="text-gray-900 mb-2">Clause 5.3: Consumables</h5>
                  <p className="text-gray-700 leading-relaxed">
                    <span className="font-medium">As per IRDAI Master Circular 2024:</span> Hospitals 
                    cannot charge separately for consumables such as gloves, syringes, masks, 
                    and IV sets. These must be included in the package cost.
                  </p>
                </div>

                <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
                  <h5 className="text-gray-900 mb-2">Clause 6.1: Service Charges</h5>
                  <p className="text-gray-700 leading-relaxed">
                    Registration charges, admission fees, and service charges are not 
                    permitted deductions under IRDAI guidelines.
                  </p>
                </div>

                <div>
                  <h5 className="text-gray-900 mb-2">Deductibles & Co-payment</h5>
                  <p className="text-gray-700 leading-relaxed">
                    No deductible applicable. No co-payment for this policy.
                  </p>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <h5 className="text-gray-900 mb-2">IRDAI Reference</h5>
                  <p className="text-gray-700 leading-relaxed text-xs">
                    Master Circular on Standardization of Health Insurance Products, 2024
                    - Section 3.4.2: Consumables and disposables must be included in 
                    hospital package and cannot be charged separately.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 bg-gray-50">
          <div className="flex justify-between items-center">
            <p className="text-sm text-gray-600">
              This is sample data to demonstrate the audit process.
            </p>
            <button
              onClick={onRunSampleAudit}
              className="bg-[#10B981] hover:bg-[#059669] text-white px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
            >
              <span>▶</span>
              Run Audit on Sample Data
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
