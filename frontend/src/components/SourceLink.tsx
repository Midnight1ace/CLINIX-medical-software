interface SourceLinkProps {
  documentId: string
  documentName: string
  onClick?: () => void
}

export default function SourceLink({ documentName, onClick }: SourceLinkProps) {
  return (
    <a href="#" onClick={(e) => {
      e.preventDefault()
      onClick?.()
    }} className="source-link">
      📄 {documentName}
    </a>
  )
}
