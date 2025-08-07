'use client'

import { useState } from 'react'

interface HeaderProps {
  user?: {
    id: string
    email: string
    full_name: string
  } | null
  onLogout: () => void
  onDeleteAccount: () => void
}

export default function Header({ user, onLogout, onDeleteAccount }: HeaderProps) {
  const [workspaceDropdownOpen, setWorkspaceDropdownOpen] = useState(false)
  const [userDropdownOpen, setUserDropdownOpen] = useState(false)

  return (
    <header className="bg-slate-800 border-b border-slate-700 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Workspace Selector */}
        <div className="relative">
          <button
            onClick={() => setWorkspaceDropdownOpen(!workspaceDropdownOpen)}
            className="flex items-center text-white hover:text-slate-200 transition-colors"
          >
            <span className="text-lg font-medium">Sales Workspace</span>
            <svg
              className="ml-2 w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>

          {workspaceDropdownOpen && (
            <div className="absolute top-full left-0 mt-2 w-64 bg-white rounded-md shadow-lg z-50 border">
              <div className="py-1">
                <div className="px-4 py-2 text-sm text-gray-700 border-b">
                  <div className="font-medium">Sales Workspace</div>
                  <div className="text-xs text-gray-500">Current workspace</div>
                </div>
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Switch Workspace
                </button>
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Create New Workspace
                </button>
              </div>
            </div>
          )}
        </div>

        {/* User Profile */}
        <div className="relative">
          <button
            onClick={() => setUserDropdownOpen(!userDropdownOpen)}
            className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-full text-white hover:bg-blue-700 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          </button>

          {userDropdownOpen && (
            <div className="absolute top-full right-0 mt-2 w-64 bg-white rounded-md shadow-lg z-50 border">
              <div className="py-1">
                <div className="px-4 py-3 text-sm text-gray-700 border-b">
                  <div className="font-medium">{user?.full_name || 'User'}</div>
                  <div className="text-xs text-gray-500">{user?.email}</div>
                </div>
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Profile Settings
                </button>
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Account Settings
                </button>
                <div className="border-t">
                  <button
                    onClick={onDeleteAccount}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                  >
                    Delete Account
                  </button>
                  <button
                    onClick={onLogout}
                    className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  >
                    Sign Out
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Close dropdowns when clicking outside */}
      {(workspaceDropdownOpen || userDropdownOpen) && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => {
            setWorkspaceDropdownOpen(false)
            setUserDropdownOpen(false)
          }}
        />
      )}
    </header>
  )
}
