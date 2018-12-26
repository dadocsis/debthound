import React from "react";

const PREV_NEXT_COUNT = 2;

class Pager extends React.Component {
    constructor(props){
        super(props);
        this.pageClick = this.pageClick.bind(this);
        this.last = this.last.bind(this);
        this.first = this.first.bind(this);
    }

    pageClick(page){
        this.props.handlePageClick(page);
    }

    last(){
        this.props.handlePageClick(this.props.totalPages)
    }

    first(){
        this.props.handlePageClick(1)
    }


    render(){
        let trailingPages = [];
        let leadingPages = [];
        let step = this.props.currentPage - PREV_NEXT_COUNT;
        let key = 0;

        for (let i=step; i < this.props.currentPage; i++){
            if (i<=0) continue;
            key++;
            trailingPages.push((<li className="page-item" key={key}>
                <button className={"page-link"} onClick={() => this.pageClick(i)}>{i}</button></li>))
        }
        //current page
        trailingPages.push((<li className="page-item active" key={0}>
                <button className={"page-link"} onClick={() => this.pageClick(this.props.currentPage)}>
                    {this.props.currentPage}</button></li>))

        for (let i=this.props.currentPage+1; i <= PREV_NEXT_COUNT + this.props.currentPage; i++){
            if (i >= this.props.totalPages) break;
            key++;
            leadingPages.push((<li className="page-item" key={key}>
                <button className="page-link" onClick={() => this.pageClick(i)}>
                    {i}</button></li>))
        }

        let prevPage = this.props.currentPage > 1 ? this.props.currentPage - 1 : 1;
        return (
            <div className="row">
                <nav aria-label="Page navigation example">
                  <ul className="pagination">
                        <li className="page-item">
                          <button className="page-link" aria-label="Previous"
                                  onClick={() => this.pageClick(prevPage)}
                                  disabled={this.props.currentPage === 1}>
                            <span aria-hidden="true">&laquo;</span>
                            <span className="sr-only">Previous</span>
                          </button>
                        </li>
                            {[...trailingPages, ...leadingPages]}
                        <li className="page-item">
                          <button className="page-link" aria-label="Next"
                                  onClick={() => this.pageClick(this.props.currentPage + 1)}
                                  disabled={this.props.currentPage === this.props.totalPages}>
                            <span aria-hidden="true">&raquo;</span>
                            <span className="sr-only">Next</span>
                          </button>
                        </li>
                  </ul>
                </nav>
                <div className="dropdown dropup">
                    <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenu2"
                            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {this.props.currentPage + ' of ' + this.props.totalPages}
                    </button>
                    <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
                        <button className="dropdown-item" type="button"
                                disabled={1 === this.props.currentPage} onClick={this.first}>First</button>
                        <button className="dropdown-item" type="button" onClick={this.last}
                                disabled={this.props.totalPages === this.props.currentPage}>Last</button>
                    </div>
                </div>
            </div>)
    }
}
export default Pager