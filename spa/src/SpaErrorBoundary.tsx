import { Component, type ErrorInfo, type ReactNode } from "react";
import { Link } from "react-router-dom";

type Props = { children: ReactNode; resetKey: string };
type State = { err: Error | null };

export class SpaErrorBoundary extends Component<Props, State> {
  state: State = { err: null };

  static getDerivedStateFromError(err: Error): State {
    return { err };
  }

  componentDidUpdate(prev: Props) {
    if (prev.resetKey !== this.props.resetKey && this.state.err) {
      this.setState({ err: null });
    }
  }

  componentDidCatch(err: Error, info: ErrorInfo) {
    console.error("[SpaErrorBoundary]", err, info.componentStack);
  }

  render() {
    if (this.state.err) {
      return (
        <div className="spa-error-fallback" role="alert">
          <h1 className="spa-error-fallback-title">壳层渲染出错</h1>
          <p className="spa-error-fallback-detail">
            {this.state.err.message || String(this.state.err)}
          </p>
          <nav className="spa-error-fallback-actions" aria-label="恢复操作">
            <Link to="/">返回总览</Link>
            <span className="spa-error-fallback-sep" aria-hidden="true">
              ·
            </span>
            <button
              type="button"
              className="spa-error-fallback-retry"
              onClick={() => this.setState({ err: null })}
            >
              重试当前页
            </button>
          </nav>
        </div>
      );
    }
    return this.props.children;
  }
}
