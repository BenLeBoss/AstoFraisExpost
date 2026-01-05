
import '../../Styles/Popups/Popup_Confirmation.css';

function ConfirmationPopup({ isOpen, message, onConfirm, onCancel }) {

  if (!isOpen) return null;

  return (
    <div className="confirmation-overlay" onClick={onCancel}>
      <div className="confirmation-popup" onClick={(e) => e.stopPropagation()}>
        <p className="confirmation-message">{message}</p>
        <div className="confirmation-buttons">
          <button className="btn btn-oui" onClick={() => onConfirm(true)}>Oui</button>
          <button className="btn btn-non" onClick={onCancel}>Non</button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmationPopup;